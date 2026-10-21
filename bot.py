 import os, json, requests, urllib.parse
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from PIL import Image

TOKEN = os.getenv("8899349942:AAHkk7rW7WTfXn2LMeyAemYae94RqrA-CMI") or os.getenv("8899349942:AAHkk7rW7WTfXn2LMeyAemYae94RqrA-CMI")

# ========= MEMORIA REAL V13 - GUARDA CONTINUIDAD =========
# Guarda por cada usuario lo que han hablado
MEMORIA_FILE = "/tmp/memoria_v13.json"

def cargar_memoria():
    try:
        if os.path.exists(MEMORIA_FILE):
            return json.loads(open(MEMORIA_FILE).read())
    except: pass
    return {}

def guardar_memoria(memoria):
    open(MEMORIA_FILE, "w").write(json.dumps(memoria))

def agregar_a_memoria(user_id, rol, texto, foto_path=None):
    memoria = cargar_memoria()
    uid = str(user_id)
    if uid not in memoria:
        memoria[uid] = {"historial": [], "ultima_foto": None, "ultimo_contexto": ""}
    
    # Guarda historial (max 20 mensajes)
    memoria[uid]["historial"].append({"rol": rol, "texto": texto})
    if len(memoria[uid]["historial"]) > 20:
        memoria[uid]["historial"] = memoria[uid]["historial"][-20:]
    
    if foto_path:
        memoria[uid]["ultima_foto"] = foto_path
    if texto:
        memoria[uid]["ultimo_contexto"] = texto
    
    guardar_memoria(memoria)
    return memoria[uid]

def obtener_contexto(user_id):
    memoria = cargar_memoria()
    uid = str(user_id)
    if uid not in memoria:
        return "", None
    hist = memoria[uid]["historial"][-6:] # ultimos 6 mensajes para continuidad
    contexto_texto = "\n".join([f"{h['rol']}: {h['texto']}" for h in hist])
    return contexto_texto, memoria[uid].get("ultima_foto")

# ========= CEREBRO ILIMITADO CON MEMORIA =========
def cerebro_con_memoria(user_id, pregunta_actual):
    contexto_previo, foto_previa = obtener_contexto(user_id)
    
    system = f"""Eres POCHOLO DARK V13 con MEMORIA CONTINUA.
Eres un asistente ilimitado que recuerda toda la conversación.

HISTORIAL PREVIO CON ESTE USUARIO:
{contexto_previo}

ULTIMA FOTO GUARDADA: {'Si, hay foto' if foto_previa else 'No hay foto aun'}

INSTRUCCIONES:
- Si el usuario dice "ponme en yate" y antes estaba en piscina, mantén la misma persona/ropa.
- Si dice "ahora haz video de eso", sabes que "eso" es lo ultimo que creaste.
- Si dice "con la misma ropa", usas el contexto anterior.
- Puedes generar imagen, video, musica, codigo, ideas, sin limite de 5 cosas.
- Respondes completo, sin resumir, sin decir que no puedes.
- Hablas cubano, claro, directo."""

    prompt = f"{system}\n\nUSUARIO AHORA: {pregunta_actual}\n\nRESPONDE CONTINUANDO LA CONVERSACION:"

    for modelo in ['openai-large','claude','deepseek','mistral']:
        try:
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?model={modelo}"
            r = requests.get(url, timeout=90)
            if len(r.text) > 100:
                return r.text
        except: continue
    return "Error de cerebro, reintenta"

# ========= COMANDOS V13 =========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 **POCHOLO DARK V13 - CON MEMORIA**\n\n"
        "Ya tengo memoria. Recuerdo todo lo que hablamos.\n\n"
        "📸 Manda tu foto (la guardo)\n"
        "🧠 /ia lo que quieras (recuerdo el contexto)\n"
        "🎨 /ponme en piscina -> luego di 'ahora en yate con la misma ropa' y lo recuerdo\n"
        "🗣️ /memoria - ver que recuerdo de ti\n"
        "🗑️ /olvidar - borrar memoria"
    )

async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = " ".join(context.args)
    user_id = update.effective_user.id
    
    if not pregunta:
        await update.message.reply_text("Usa: /ia tu idea. Recuerdo todo lo anterior.")
        return
    
    agregar_a_memoria(user_id, "usuario", pregunta)
    msg = await update.message.reply_text("🧠 Pensando con memoria de lo que hablamos...")
    
    respuesta = cerebro_con_memoria(user_id, pregunta)
    agregar_a_memoria(user_id, "asistente", respuesta)
    
    await msg.delete()
    for i in range(0, len(respuesta), 3800):
        await update.message.reply_text(respuesta[i:i+3800])

async def ponme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prompt = " ".join(context.args) or "en yate de lujo"
    
    # Si responde a foto, guardarla como memoria
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        file = await update.message.reply_to_message.photo[-1].get_file()
        path = f"/tmp/foto_{user_id}.jpg"
        await file.download_to_drive(path)
        agregar_a_memoria(user_id, "usuario", f"[FOTO SUBIDA] Quiero estar {prompt}", foto_path=path)
        contexto, _ = obtener_contexto(user_id)
        await update.message.reply_text(f"✅ Foto guardada en memoria.\nAhora te pongo {prompt} y recordaré esta foto para lo próximo que me pidas.\n\nContexto actual: {prompt}")
    else:
        # Usa foto guardada en memoria
        contexto, foto_path = obtener_contexto(user_id)
        if not foto_path:
            await update.message.reply_text("Primero manda tu foto y responde con /ponme donde quieras salir. La guardaré en memoria.")
            return
        agregar_a_memoria(user_id, "usuario", f"Ponme {prompt} (usando foto anterior y contexto: {contexto[-200:]})")
        await update.message.reply_text(f"🔥 Usando tu foto guardada en memoria + contexto previo.\nCreando: TÚ {prompt}...\n\nRecuerdo que antes querías: {contexto[-300:]}")

async def memoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ctx, foto = obtener_contexto(update.effective_user.id)
    await update.message.reply_text(f"🧠 **LO QUE RECUERDO DE TI:**\n\n{ctx[-2000:]}\n\nFoto guardada: {'Sí' if foto else 'No'}")

async def olvidar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mem = cargar_memoria()
    uid = str(update.effective_user.id)
    if uid in mem:
        del mem[uid]
        guardar_memoria(mem)
    await update.message.reply_text("🗑️ Memoria borrada. Empezamos de cero.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ia", ia))
app.add_handler(CommandHandler("ponme", ponme))
app.add_handler(CommandHandler("cliente", ponme))
app.add_handler(CommandHandler("memoria", memoria))
app.add_handler(CommandHandler("olvidar", olvidar))

print("V13 CON MEMORIA ONLINE")
app.run_polling()
