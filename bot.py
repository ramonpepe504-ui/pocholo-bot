import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN") or "PEGA_AQUI_TU_TOKEN"

async def start(update, context):
    await update.message.reply_text("✅ Bot 24/7 prendido!\nUsa /fake +54... | comidas online | mensaje")

async def fake(update, context):
    txt = ' '.join(context.args)
    await update.message.reply_text(f"📸 Fake Redmi 9A:\n{txt}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("fake", fake))
app.run_polling()
