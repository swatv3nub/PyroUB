from pyroub import *
from core.helpers.pyrohelper import get_arg
from io import BytesIO
from pyrogram import filters

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with session.post(url, json={"code": code}) as result:
        img = BytesIO(await result.read())
        img.name = "PyroUB.png"
        return img
        
@app.on_message(cmd("carbon") & filters.user(AUTH))
async def carbon(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.text:
            await eor(message, "Reply to a text message to make carbon or Give some texts")
            return
        else:
            text = message.reply_to_message.text
    else:
        try:
            text = get_arg(message)
        except:
            await eor(message, "Reply to a text message to make carbon or Give some texts")
            return
    m = await eor(message, "Being Carbonised...")
    carbon = await make_carbon(text)
    await app.send_document(message.chat.id, carbon)
    await m.delete()
    carbon.close()