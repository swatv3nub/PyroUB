import asyncio

import pybase64 as b64
from pyrogram import filters
from pyroub import *


@app.on_message(cmd("encode") & filters.user(AUTH))
async def enc(_, message):
    if not message.reply_to_message:
        await eor(message, "Reply to a Text Message!")
        return
    else:
        text = message.reply_to_message.text
        encoded = str(b64.b64encode(bytes(text, "utf-8")))[2:-1]
        await eor(message, "Encoded in Base64: 👇👇")
        await app.send_message(message.chat.id, encoded)
        await asyncio.sleep(2)
        try:
            await message.delete()
        except:
            pass
        
@app.on_message(cmd("decode") & filters.user(AUTH))
async def dec(_, message):
    if not message.reply_to_message:
        await eor(message, "Reply to a Text Message!")
        return
    else:
        text = message.reply_to_message.text
        decoded = str(b64.b64decode(bytes(text, "utf-8"), validate=True))[2:-1]
        await eor(message, "Decoded from Base64: 👇👇")
        await app.send_message(message.chat.id, decoded)
        await asyncio.sleep(2)
        try:
            await message.delete()
        except:
            pass
