from pyrogram import filters
from pyroub import *


@app.on_message(cmd("webss") & filters.user(AUTH))
async def ss(_, message):
    try:
        if len(message.command) != 2:
            return await eor(message, "Give A Url To Fetch Screenshot.")
        url = message.text.split(None, 1)[1]
        m = await eor(message, "Taking Screenshot")
        try:
            await message.reply_photo(
                photo=f"https://webshot.amanoteam.com/print?q={url}",
                quote=False,
            )
        except TypeError:
            return await m.edit("Invalid Website")
        await m.delete()
    except Exception as e:
        await eor(message, str(e))