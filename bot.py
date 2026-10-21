import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
from PIL import Image, ImageDraw

TOKEN = "8899349942:AAES4zwAfDXI6L8zFbbKZv4cYTt85mWH5qo"  # <--- SOLO ESTO TIENES QUE PONER

# Crea logo si no existe
if not os.path.exists('menu3d.png'):
    try:
        img = Image.new('RGB', (900, 450), (15,0,35))
        d = ImageDraw.Draw(img)
        d.rectangle([(10,10),(890,440)], outline=(0,255,255), width=5)
        d.text((40,40), "POCHOLO DARK KING KONG", fill=(0,255,255))
        d.text((40,150), "CEREBRO IA V8 - ILIMITADO", fill=(255,255,255))
        d.text((40,250), "No gasta polen - Cuba Ready", fill=(255,0,255))
        img.save('menu3d.png')
    except: pass

MENU = "👑 POCHOLO DARK V8 - CEREBRO ILIMITADO 🧠\n\n🧠 /ia pregunta\n💻 /code hazme algo\n▶️ /start menu\n\nEste cerebro NO SE ACABA nunca."

def botones(): return InlineKeyboardMarkup([[InlineKeyboardButton("🧠 IA", callback_data='a'), InlineKeyboardButton("💻 CODE", callback_data='b')]])

async def start(u,c):
    try:
        with open('menu3d.png','rb') as f: await u.message.reply_photo(f, caption=MENU, reply_markup=botones())
    except: await u.message.reply_text(MENU, reply_markup=botones())

async def ia(u,c):
    pregunta = " ".join(c.args)
    if not pregunta: await u.message.reply_text("Usa: /ia hazme una pagina web"); return
    await u.message.reply_text("🧠 Programando... ⏳")
    # 3 CEREBROS DE RESPALDO - si falla uno, entra el otro
    cerebros = [
        f"https://text.pollinations.ai/{requests.utils.quote(f'Eres POCHOLO DARK, programador senior cubano, nivel Meta AI. Das codigo completo funcional sin dejar ... Explicas paso a paso. Pregunta: {pregunta}')}",
        f"https://text.pollinations.ai/{requests.utils.quote(pregunta)}?model=openai-large&system=Eres%20POCHOLO%20DARK%20programador%20senior%20cubano%20nivel%20Dios,%20das%20codigo%20completo%20funcional",
        f"https://text.pollinations.ai/{requests.utils.quote(pregunta)}?model=mistral"
    ]
    for url in cerebros:
        try:
            r = requests.get(url, timeout=60)
            if r.status_code==200 and len(r.text)>20:
                txt=r.text
                for i in range(0,len(txt),3900): await u.message.reply_text(txt[i:i+3900])
                return
        except Exception as e: print(e); continue
    await u.message.reply_text("Todos los cerebros fallaron, intenta de nuevo en 10 seg")

async def code(u,c):
    p=" ".join(c.args)
    c.args=[f"DAME CODIGO COMPLETO EN PYTHON 100% FUNCIONAL, LISTO PARA COPIAR PEGAR, SIN PONER '...', EXPLICA PASO A PASO EN CUBANO: {p}"]
    await ia(u,c)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", start))
app.add_handler(CommandHandler("ia", ia))
app.add_handler(CommandHandler("code", code))
app.add_handler(CallbackQueryHandler(lambda u,c: u.callback_query.answer()))

print("V8 ILIMITADO ONLINE")
app.run_polling()
