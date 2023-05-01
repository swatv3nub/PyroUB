from pyrogram import filters
from inspect import getfullargspec
from pyroub import *

@app.on_message(cmd("tr") & filters.user(AUTH))
async def translate(_, message):
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        if len(message.text.split()) == 1:
            await eor(message, text=f"Usage: Reply to a message, then `{PREFIX}tr <lang>`")
            return
        target = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        detectlang = translate.detect(text)
        try:
            awoo = translate.translate(text, lang_tgt=target)
        except ValueError as e:
            await eor(message, text=f"Error: {str(e)}")
            return
    else:
        if len(message.text.split()) <= 2:
            await eor(message, text=f"Usage: `{PREFIX}tr <lang> <text>`")
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        detectlang = translate.detect(text)
        try:
            awoo = translate.translate(text, lang_tgt=target)
        except ValueError as e:
            await eor(message, text=f"Error: {str(e)}")
            return
    await eor(
        message,
        text=f"Translated from {detectlang[0]} to {target}:\n{awoo}",
    )
    return
