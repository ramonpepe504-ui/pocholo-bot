import os
import json
import requests
import urllib.parse
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Lee el token del panel Entorno
TOKEN = os.getenv("8899349942:AAHzVOEII3FQ5csVeMmxCJz2niUXfASrcO4")
if not TOKEN:
    print("❌ Falta BOT_TOKEN en Entorno")
    exit(1)

MEMORIA_FILE = "/tmp/memoria_v13.json"

def cargar_memoria():
    try:
        if os.path.exists(MEMORIA_FILE):
            with open(MEMORIA_FILE, "r") as f:
                return json.load(f)
    except:
        pass
    return {}

def guardar_memoria(memoria):
    try:
        with open(MEMORIA_FILE, "w") as f:
            json.dump(memoria, f)
    except:
        pass

def agregar_memoria(user_id, rol, texto):
    memoria = cargar_memoria()
    uid = str(user_id)
    if uid not in memoria:
        memoria[uid] = []
    memoria[uid].append({"rol": rol, "texto": texto})
    if len(memoria[uid]) > 20:
        memoria[uid] = memoria[uid][-20:]
    guardar_memoria(memoria)
    return memoria[uid]

def obtener_contexto(user_id):
    memoria = cargar_memoria()
    historial = memoria.get(str(user_id), [])[-6:]
    return "\n".join([f"{h['rol']}: {h['texto']}" for h in historial])

def cerebro_ilimitado(user_id, pregunta):
    contexto = obtener_contexto(user_id)
    system = f"""Eres POCHOLO DARK V13 UNIVERSAL con memoria.
Historial:
{contexto}
Eres ilimitado, sin limite de 5 cosas, recuerdas todo."""
    prompt = f"{system}\nUsuario: {pregunta}"
    for modelo in ['openai-large','claude','deepseek','mistral-large']:
        try:
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?model={modelo}"
            r = requests.get(url, timeout=60)
            if r.status_code == 200 and len(r.text) > 100:
                return r.text
        except:
            continue
    return "Prueba de nuevo en 10 seg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 V13 CORREGIDO ONLINE\n"
        "✅ Token OK\n"
        "✅ Memoria OK\n\n"
        "/ia lo que quieras\n"
        "/ponme en piscina (responde a foto)\n"
        "/cliente en yate\n"
        "/memoria\n"
        "/olvidar"
    )

async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = " ".join(context.args)
    if not pregunta:
        await update.message.reply_text("Usa: /ia tu idea completa")
        return
    agregar_memoria(update.effective_user.id, "usuario", pregunta)
    msg = await update.message.reply_text("🧠 Pensando...")
    resp = cerebro_ilimitado(update.effective_user.id, pregunta)
    agregar_memoria(update.effective_user.id, "asistente", resp)
    await msg.delete()
    for i in range(0, len(resp), 3800):
        await update.message.reply_text(resp[i:i+3800])

async def ponme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prompt_c = " ".join(context.args) or "en yate de lujo"
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        file = await update.message.reply_to_message.photo[-1].get_file()
        path = f"/tmp/foto_{user_id}.jpg"
        await file.download_to_drive(path)
        agregar_memoria(user_id, "usuario", f"[FOTO] Quiero {prompt_c}")
        await update.message.reply_text(f"✅ Foto guardada para: {prompt_c}\nYa recuerdo tu cara.")
    else:
        ctx = obtener_contexto(user_id)
        if not ctx:
            await update.message.reply_text("📸 Manda foto y responde /ponme en yate / piscina / moto")
            return
        agregar_memoria(user_id, "usuario", f"Ponme {prompt_c}")
        await update.message.reply_text(f"🔥 Usando memoria.\nPedido: {prompt_c}\nRecuerdo: {ctx[-500:]}")

async def ver_memoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ctx = obtener_contexto(update.effective_user.id)
    await update.message.reply_text(f"🧠 Recuerdo:\n\n{ctx[-3500:] or 'Nada aun'}")

async def olvidar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mem = cargar_memoria()
    uid = str(update.effective_user.id)
    if uid in mem:
        del mem[uid]
        guardar_memoria(mem)
    await update.message.reply_text("🗑️ Memoria borrada")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ia", ia))
app.add_handler(CommandHandler("ponme", ponme))
app.add_handler(CommandHandler("cliente", ponme))
app.add_handler(CommandHandler("editar", ponme))
app.add_handler(CommandHandler("memoria", ver_memoria))
app.add_handler(CommandHandler("olvidar", olvidar))
print(f"✅ BOT V13 ONLINE - Token ...{TOKEN[-6:]}")
app.run_polling()
