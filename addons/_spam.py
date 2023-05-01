"""Use this at your own risk"""

import asyncio
from pyroub import *
from pyrogram import filters
from core.helpers.pyrohelper import get_arg

@app.on_message(cmd("spam") & filters.me)
async def spam(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.text:
            await eor(message, "Reply to a text message")
            return
        else:
            text = message.reply_to_message.text
        try:
            count = get_arg(message)
        except:
            await eor(message, "Give No of Messages to send!")
            return
    else:
        try:
            count = message.text.split(" ")[1]
        except IndexError:
            await eor(message, "Give Number of Messages")
            return
        try:
            text = message.text.split(" ", 2)[2]
        except IndexError:
            await eor(message, "What is the Message?")
            return
    if not count.isnumeric():
        await eor(message, "Give a Digit")
        return
    count = int(count)
    for i in range(count):
        await app.send_message(message.chat.id, text)
        await asyncio.sleep(1)