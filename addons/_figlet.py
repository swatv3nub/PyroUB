from pyroub import *
from pyrogram import filters
from core.helpers.pyrohelper import get_arg
from core.helpers.figlet import *

@app.on_message(cmd("figlet") & filters.user(AUTH))
async def figlet(_, message):
    try:
        font = message.text.split(" ")[1]
    except IndexError:
        await eor(message, "No Fonts Given, Taking the default one!")
        font = "rev"
    if font not in CMD_SET:
        font = None
        await eor(message, "Invalid Font, Taking the default one!")

    if not font:
        font = "rev"
        text = get_arg(message)
    else:
        font = font
        text = message.text.split(" ", 2)[2]
        
    font = CMD_SET[font]
    res = figlet(text, font=font)
    await eor(message, res)