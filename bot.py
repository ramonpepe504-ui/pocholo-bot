import requests, urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from PIL import Image, ImageDraw

TOKEN = "8899349942:AAES4zwAfDXI6L8zFbbKZv4cYTt85mWH5qo"

# Logo auto-creado
if not os.path.exists('menu3d.png'):
    try:
        img = Image.new('RGB', (900, 500), (10,0,30))
        d = ImageDraw.Draw(img)
        d.rectangle([(10,10),(890,490)], outline=(0,255,255), width=5)
        d.text((30,30), "POCHOLO DARK V9", fill=(0,255,255))
        d.text((30,100), "GROK BOT CUBANO", fill=(255,0,255))
        d.text((30,180), "MULTI-CEREBRO", fill=(255,255,0))
        d.text((30,250), "Claude + Grok + Mistral", fill=(255,255,255))
        d.text((30,330), "Como el original de Elon", fill=(200,200,200))
        img.save('menu3d.png')
    except: pass

MENU = """
👑 POCHOLO DARK V9 - GROK BOT CUBANO 🇨🇺🧠

🧬 MULTI-CEREBRO ACTIVO:
🧠 Claude - razonamiento
⚡ Grok 4.7 - programación
🎨 Mistral - rápido

COMANDOS:
🧠 /ia pregunta - Elige cerebro solo
💻 /code hazme X - Fuerza modo programador
🎨 /img un gato en la habana - Genera imagen
▶️ /start - Menu

Ejemplo: /ia crea un bot que descarga de youtube
"""

def botones(): 
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 IA MULTI", callback_data='1'), InlineKeyboardButton("💻 CODE", callback_data='2')],
        [InlineKeyboardButton("🎨 IMAGEN", callback_data='3')]
    ])

async def start(u,c):
    try:
        with open('menu3d.png','rb') as f: await u.message.reply_photo(f, caption=MENU, reply_markup=botones())
    except: await u.message.reply_text(MENU, reply_markup=botones())

# --- GROK BOT LOGIC: ELIGE EL MEJOR CEREBRO SOLO ---
def grok_multi_cerebro(pregunta):
    pregunta_lower = pregunta.lower()
    
    # Si pide codigo -> usa cerebro de codigo
    if any(x in pregunta_lower for x in ['codigo','bot','python','programa','script','html','api','calculadora','login']):
        models = ['openai-large', 'openai', 'deepseek']
        system = "Eres POCHOLO DARK, programador senior nivel Dios, como Grok 4.7 + Claude Opus 5.5. Das SIEMPRE codigo completo funcional 100% listo para copiar/pegar, sin dejar ... Explicas paso a paso en cubano."
    # Si pide razonamiento complejo
    elif any(x in pregunta_lower for x in ['explica','por que','analiza','que es','como funciona']):
        models = ['claude', 'openai-large', 'mistral']
        system = "Eres POCHOLO DARK, con cerebro Claude Opus 5.5 + Grok 4.7. Razonas paso a paso, verificas tu trabajo, das respuestas profundas y claras en español cubano."
    # Si es simple -> rápido
    else:
        models = ['openai', 'mistral', 'openai-large']
        system = "Eres POCHOLO DARK, asistente rápido y útil, como Meta AI, respondes corto y directo en cubano."

    for model in models:
        try:
            url = f"https://text.pollinations.ai/{urllib.parse.quote(pregunta)}?model={model}&system={urllib.parse.quote(system)}"
            r = requests.get(url, timeout=70)
            if r.status_code == 200 and len(r.text) > 30:
                return f"🧠 Cerebro usado: {model.upper()} (Grok Multi)\n\n{r.text}"
        except Exception as e:
            print(f"Fallo {model}: {e}")
            continue
    return "❌ Todos los cerebros ocupados, intenta de nuevo"

async def ia(u,c):
    pregunta = " ".join(c.args)
    if not pregunta: await u.message.reply_text("Usa: /ia hazme un bot de youtube"); return
    msg = await u.message.reply_text("🧬 Grok Multi eligiendo mejor cerebro... ⏳")
    respuesta = grok_multi_cerebro(pregunta)
    try: await msg.delete()
    except: pass
    for i in range(0, len(respuesta), 3900):
        await u.message.reply_text(respuesta[i:i+3900])

async def code(u,c):
    p = " ".join(c.args) or "hola"
    c.args = [f"CODIGO COMPLETO PYTHON FUNCIONAL, LISTO PARA USAR, SIN ... : {p}"]
    await ia(u,c)

async def img(u,c):
    prompt = " ".join(c.args)
    if not prompt: await u.message.reply_text("Usa: /img un gato con sombrero en La Habana, 3D neon"); return
    await u.message.reply_text("🎨 Generando con Midjourney-style... ⏳")
    try:
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?model=turbo&width=1024&height=1024&nologo=true"
        await u.message.reply_photo(url, caption=f"🎨 {prompt}\n🧠 Cerebro: Midjourney (via Pollinations)")
    except Exception as e: await u.message.reply_text(f"Error imagen: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", start))
app.add_handler(CommandHandler("ia", ia))
app.add_handler(CommandHandler("code", code))
app.add_handler(CommandHandler("img", img))

print("POCHOLO V9 GROK BOT ONLINE")
app.run_polling()
