import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from PIL import Image, ImageDraw, ImageFont
import io, os

TOKEN = "8899349942:AAES4zwAfDXI6L8zFbbKZv4cYTt85mWH5qo"
POLLI_KEY = "sk_9TIMuCKYa3NXGnvfQFKAB4wIBkirF8Oo"

# --- Crea el logo 3D si no existe ---
def crear_menu3d():
    if os.path.exists('menu3d.png'):
        return
    try:
        img = Image.new('RGB', (800, 400), color=(10, 10, 25))
        draw = ImageDraw.Draw(img)
        # Fondo neón
        draw.rectangle([(0,0),(800,400)], fill=(20,0,40))
        draw.rectangle([(20,20),(780,380)], outline=(0,255,255), width=4)
        draw.text((50, 50), "POCHOLO DARK", fill=(0,255,255))
        draw.text((50, 120), "KING KONG", fill=(255,0,255))
        draw.text((50, 200), "CEREBRO IA CUBA - ONLINE", fill=(255,255,255))
        draw.text((50, 280), "Hecho por ti, pa' Cuba", fill=(200,200,200))
        img.save('menu3d.png')
        print("menu3d.png creado")
    except Exception as e:
        print(f"No se pudo crear imagen: {e}")

crear_menu3d()

MENU_TEXTO = """
👑 POCHOLO DARK KING KONG - CEREBRO IA 🧠🇨🇺

🧠 /ia + pregunta - Cerebro programador
💻 /code + lo que quieras - Te codea completo
▶️ /start - Menú con logo 3D
"""

def get_botones():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🧠 CEREBRO IA", callback_data='ia'), InlineKeyboardButton("💻 CODE", callback_data='code')]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open('menu3d.png', 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=MENU_TEXTO, reply_markup=get_botones())
    except Exception as e:
        print(e)
        await update.message.reply_text(MENU_TEXTO, reply_markup=get_botones())

async def ia_cerebro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = " ".join(context.args)
    if not pregunta:
        await update.message.reply_text("🧠 Usa: /ia hazme un bot que descargue videos de youtube en python")
        return
    await update.message.reply_text("🧠 Pensando en modo programador destructor cubano... ⏳")
    try:
        headers = {"Authorization": f"Bearer {POLLI_KEY}", "Content-Type": "application/json"}
        # MODELO BUENO PARA CODIGO
        data = {
            "model": "openai-large",
            "messages": [
                {"role": "system", "content": "Eres POCHOLO DARK, programador senior nivel Dios como Meta AI. Experto en Python, Telegram bots, APIs. Si el usuario pide codigo, SIEMPRE das el codigo completo, listo para copiar/pegar, funcional, sin dejar partes con '...'. Explicas paso a paso en español cubano."},
                {"role": "user", "content": pregunta}
            ],
            "stream": False
        }
        r = requests.post("https://gen.pollinations.ai/v1/chat/completions", headers=headers, json=data, timeout=90)
        print("RESPUESTA POLLI:", r.text[:500])
        j = r.json()
        respuesta = j['choices'][0]['message']['content']

        # Enviar en trozos
        for i in range(0, len(respuesta), 3900):
            await update.message.reply_text(respuesta[i:i+3900])
    except Exception as e:
        await update.message.reply_text(f"Error cerebro: {e}\nRevisa logs")

async def code_cerebro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = " ".join(context.args)
    if not pregunta:
        await update.message.reply_text("💻 Usa: /code crea una calculadora con tkinter")
        return
    context.args = [f"CREAME ESTO CON CODIGO COMPLETO FUNCIONAL EN PYTHON, EXPLICAME PASO A PASO COMO LO HICISTE, NO DEJES PARTES VACIAS: {pregunta}"]
    await ia_cerebro(update, context)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE): await start(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("ia", ia_cerebro))
app.add_handler(CommandHandler("code", code_cerebro))
app.add_handler(CallbackQueryHandler(lambda u,c: u.callback_query.answer()))

print("POCHOLO V7 - LOGO + CODE FIX OK")
app.run_polling()
