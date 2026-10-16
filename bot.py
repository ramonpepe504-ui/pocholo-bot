from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image, ImageDraw
import io

# ========= PON TU TOKEN AQUÍ ABAJO =========
TOKEN = "8899349942:AAES4zwAfDXI6L8zFbbKZv4cYTt85mWH5qo"
# Ejemplo: TOKEN = "7991234567:AAHqwertyuiop1234567890abcdef"
# ============================================

MENU_TEXTO = """
👑 POCHOLO DARK KING KONG - DESTRUCTOR DE SISTEMAS 👑
✅ Bot 24/7 Online - Versión 3D

📋 MENÚ:
▶️ /start - Ver menú 3D destructor
📜 /menu - Ver menú de nuevo
🎭 /fake + texto - Crear broma legal
❓ /help - Ayuda
🍔 /comida - Próximamente comidas online

Todo lo anterior sigue funcionando igual!
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open('menu3d.png', 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=MENU_TEXTO)
    except:
        await update.message.reply_text(MENU_TEXTO)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MENU_TEXTO)

async def fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(context.args)
    if not texto:
        await update.message.reply_text("Usa: /fake hola bro\n\n" + MENU_TEXTO)
        return

    img = Image.new('RGB', (600, 350), color=(20, 20, 30))
    draw = ImageDraw.Draw(img)
    fecha = datetime.now().strftime("%d/%m/%Y")
    draw.rectangle([(0,0), (600, 60)], fill=(0, 200, 255))
    draw.text((10, 15), f"🎭 BROMA - NO ES REAL - {fecha}", fill=(0,0,0))
    draw.rectangle([(20, 80), (580, 280)], fill=(255,255,255), outline=(0,200,255), width=2)
    draw.text((30, 90), "Contacto Broma:", fill=(100,100,100))
    draw.text((30, 120), texto, fill=(0,0,0))
    draw.text((20, 310), "Hecho con pocholo-bot", fill=(120,120,120))

    bio = io.BytesIO()
    bio.name = 'broma.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    await update.message.reply_photo(photo=bio, caption="✅ Broma generada!")

async def comida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🍔 Próximamente: comidas online\nPor ahora usa /fake y /menu")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("fake", fake))
app.add_handler(CommandHandler("comida", comida))

print("POCHOLO BOT 24/7 3D - TODO MANTENIDO + NUEVO!")
app.run_polling()
