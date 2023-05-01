import os
import qrcode as qr
from pyroub import *
from pyrogram import filters

@app.on_message(cmd("qr") & filters.user(AUTH))
async def makeqr(_, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        elif message.reply_to_message.caption:
            text = message.reply_to_message.caption
        else:
            await message.edit("QR works with Text Messages only!")
            return
    else:
        sus = message.text.split(" ", 1)
        try:
            text = sus[1]
        except IndexError:
            await message.edit("Give Some text or reply to a message")
            return
    img = qr.make(text)
    img.save("./DOWNLOADS/PyroUB.png")
    await app.send_photo(message.chat.id, photo="./DOWNLOADS/PyroUB.png")
    os.remove("./DOWNLOADS/PyroUB.png")