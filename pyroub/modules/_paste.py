"""Themks to Hamker once again!"""
import re
import os
import aiofiles
from pyroub import *
from pyrogram import filters
from core.helpers.ezupdev import paste

pattern = re.compile(
    r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$"
)

@app.on_message(cmd(["paste", "neko", "ezup"]) & filters.user(AUTH))
async def ezup(_, message):
    if not message.reply_to_message:
        await message.edit("Reply to a Text Message or a .txt file")
        return
    await message.edit("Pasting...")
    if message.reply_to_message.text:
        content = str(message.reply_to_message.text)
    elif message.reply_to_message.document:
        doc = message.reply_to_message.document
        if doc.file_size > 10485756:
            await message.edit("Max File paste size is 1MB!")
            return
        if not pattern.search(doc.mime_type):
            await message.edit("Only Text Files can be Pasted!")
            return
        file = await message.reply_to_message.download()
        async with aiofiles.open(file, mode="r") as owo:
            content = owo.read()
            os.remove(file)
        link = await paste(content)
        await message.edit(f"Pasted to [ezup.dev]({link})!")
