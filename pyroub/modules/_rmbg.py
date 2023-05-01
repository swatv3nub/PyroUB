import os
import shutil
import asyncio
from pyroub import *
from pyrogram import filters
from removebg import RemoveBg
from core.helpers.pyrohelper import ReplyCheck

@app.on_message(cmd("rmbg") & filters.user(AUTH))
async def removebg(_, message):
    if not RMBG_API:
        await message.edit("Get the API from [remove.bg](https://remove.bg/api)", disable_web_page_preview=True)
        return
    if not message.reply_to_message:
        await message.edit("Reply to a Picture to remove the BG!")
        return
    is_reply = message.reply_to_message
    if (
        is_reply
        and is_reply.media
        and (
            is_reply.photo
            or (is_reply.document and "image" in is_reply.document.mime_type)
        )
    ):
        if os.path.exists("./DOWNLOADS/pyroUB.jpg"):
            os.remove("./DOWNLOADS/pyroUB.jpg")
        path = await app.download_media(message=is_reply, file_name="./DOWNLOADS/pyroUB.jpg")
        await message.edit("Removing BG...")
        try:
            rmbg = RemoveBg(RMBG_API, "rmbg_error.log")
            rmbg.remove_background_from_img_file(path)
            bg_less = path + "_rmbg.png"
            img = path.replace(".jpg", "_PyroUB.png")
            shutil.move(bg_less, img)
            await app.send_document(
                chat_id=message.chat.id,
                document=img,
                caption="Removed using PyroUB",
                reply_to_message_id=ReplyCheck(is_reply),
            )
            await message.delete()
            os.remove(img)
            os.remove(path)
        except Exception as e:
            await message.edit("Error Occured, Check Logs Chat!")   
            await app.send_message(LOG_CHAT, f"**RemoveBG Error:**\n{e}")
    return
