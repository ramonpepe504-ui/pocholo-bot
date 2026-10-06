import telebot, os, time, urllib.parse, random
TOKEN="8899349942:AAEgShpwgv6-gHBV0frl0xATLCcETnieDaQ"
bot=telebot.TeleBot(TOKEN)
BASE="/tmp"
os.makedirs(BASE, exist_ok=True)

def get_last(cid):
    p=os.path.join(BASE, f"last_{cid}.txt")
    return open(p).read().strip() if os.path.exists(p) else None
def set_last(cid, ruta):
    open(os.path.join(BASE, f"last_{cid}.txt"),'w').write(ruta)

def hacer_video(ruta_foto, cid, prompt="animacion"):
    bot.send_message(cid, f"🎬 ANIMANDO TU FOTO - 6 seg")
    ruta_v=os.path.join(BASE, f"V_{int(time.time())}.mp4")
    cmd=f'ffmpeg -y -loop 1 -i "{ruta_foto}" -vf "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z=\'min(zoom+0.002,1.5)\':d=1:x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':s=1280x720:fps=30" -t 6 -c:v libx264 -pix_fmt yuv420p "{ruta_v}"'
    os.system(cmd)
    if os.path.exists(ruta_v):
        bot.send_video(cid, open(ruta_v,'rb'), caption=f"✅ VIDEO ANIMADO REAL\n{prompt}")
        os.remove(ruta_v)

@bot.message_handler(content_types=['photo'])
def foto(m):
    f=bot.get_file(m.photo[-1].file_id)
    data=bot.download_file(f.file_path)
    ruta=os.path.join(BASE, f"foto_{int(time.time())}.jpg")
    open(ruta,'wb').write(data)
    set_last(m.chat.id, ruta)
    cap=m.caption.lower() if m.caption else ""
    if "anim" in cap:
        hacer_video(ruta, m.chat.id, cap)
    else:
        bot.send_message(m.chat.id, "📸 Foto guardada. Escribe: animacion")

@bot.message_handler(func=lambda m: True)
def texto(m):
    if "anim" in m.text.lower():
        r=get_last(m.chat.id)
        if r and os.path.exists(r):
            hacer_video(r, m.chat.id, m.text)
        else:
            bot.send_message(m.chat.id, "❌ Primero manda foto")
    else:
        pe=urllib.parse.quote(m.text+", ultra realistic, 8k")
        for i in range(1,4):
            url=f"https://image.pollinations.ai/prompt/{pe}?width=1024&height=1024&model=flux&seed={random.randint(1,9999999)}"
            try:
                bot.send_photo(m.chat.id, url, caption=f"OPCION {i}")
            except: pass

print("BOT CLOUD INICIADO")
bot.infinity_polling()