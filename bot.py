import requests, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from PIL import Image, ImageDraw
import io

# ========= PEGA TUS 2 CLAVES AQUÍ =========
TOKEN = "8899349942:AAES4zwAfDXI6L8zFbbKZv4cYTt85mWH5qo"
POLLI_KEY = "sk_rCGcoyhBE3vWlDQ2uExT6nEBDHFEPAqn"
# =========================================

MENU_TEXTO = """
👑 POCHOLO DARK KING KONG - CEREBRO IA ACTIVADO 🧠🇨🇺

📋 MENÚ:
🧠 /ia + pregunta - Cerebro como Meta AI
💻 /code + lo que quieras - Te programa
▶️ /start - Menú
"""

def get_botones():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🧠 CEREBRO IA", callback_data='ia')]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU_TEXTO, reply_markup=get_botones())

async def ia_cerebro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = " ".join(context.args)
    if not pregunta:
        await update.message.reply_text("🧠 Usa: /ia hazme un bot que mande fotos\n💻 /code crea una calculadora en python")
        return
    await update.message.reply_text("🧠 Pensando como programador senior... ⏳")
    try:
        headers = {"Authorization": f"Bearer {POLLI_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "openai",
            "messages": [
                {"role": "system", "content": "Eres POCHOLO DARK, programador senior nivel Dios, como Meta AI. Experto en Python y Telegram bots. Respondes en español cubano, calle, explicas paso a paso y das código completo listo para copiar/pegar."},
                {"role": "user", "content": pregunta}
            ]
        }
        r = requests.post("https://gen.pollinations.ai/v1/chat/completions", headers=headers, json=data, timeout=60)
        print(r.text)
        respuesta = r.json()['choices'][0]['message']['content']
        for i in range(0, len(respuesta), 4000):
            await update.message.reply_text(respuesta[i:i+4000])
    except Exception as e:
        await update.message.reply_text(f"Error: {e}\nRevisa que copiaste bien la POLLI_KEY")

async def code_cerebro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = " ".join(context.args) or "hola"
    context.args = [f"PROGRAMAME CODIGO COMPLETO Y EXPLICAME PASO A PASO: {pregunta}"]
    await ia_cerebro(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ia", ia_cerebro))
app.add_handler(CommandHandler("code", code_cerebro))
app.add_handler(CallbackQueryHandler(lambda u,c: u.callback_query.answer()))

print("POCHOLO V6 - CEREBRO POLLINATIONS ACTIVADO")
app.run_polling()
