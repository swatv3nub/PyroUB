import os
from pyroub import *
from pyrogram import filters
from telegraph import upload_file
from core.helpers.pyrohelper import get_arg

@app.on_message(cmd("tg") & filters.user(AUTH))
async def telegraph(_, message):
    if not message.reply_to_message:
        await message.edit("Reply to a message to upload in telegraph!")
        return
    try:
        opt = get_arg(message)
    except:
        await message.edit("Give an option, -p, -v or -g")
    if opt.lower() == "-p":
        if not message.reply_to_message.photo:
            await message.edit("-p works for photos only! Reply to a photo")
            return
        await message.edit("Uploading to Telegraph...")
        path = ("./DOWNLOADS/pyroUB.jpg")
        path = await app.download_media(message.reply_to_message, path)
        try:
            limnk = upload_file(path)
            await message.edit(f"Successfully Uploaded to [Telegraph](https://telegra.ph{limnk[0]})")
            os.remove(path)
        except:
            await message.edit("Something went Wrong!")
    elif opt.lower() == "-v":
        if not message.reply_to_message.video:
            await message.edit("-v works for videos only! Reply to a video.")
            return
        if(message.reply_to_message.video.file_size < 5242880):
            await message.edit("Uploading to Telegraph...")
            path = ("./DOWNLOADS/pyroUB.mp4")
            path = await app.download_media(message.reply_to_message, path)
            try:
                limnk = upload_file(path)
                await message.edit(f"Successfully Uploaded to [Telegraph](https://telegra.ph{limnk[0]})")
                os.remove(path)
            except:
                await message.edit("Something went Wrong!")
        else:
            await message.edit("Size should be less than 5MB.")
            return
    elif opt.lower() == "-g":
        if not message.reply_to_message.animation:
            await message.edit("-g works for GIFs only! Reply to a GIF.")
            return
        if(message.reply_to_message.animation.file_size < 5242880):
            await message.edit("Uploading to Telegraph...")
            path = ("./DOWNLOADS/pyroUB.mp4")
            path = await app.download_media(message.reply_to_message, path)
            try:
                limnk = upload_file(path)
                await message.edit(f"Successfully Uploaded to [Telegraph](https://telegra.ph{limnk[0]})")
                os.remove(path)
            except:
                await message.edit("Something went Wrong!")
        else:
            await message.edit("Size should be less than 5MB.")
            return
    else:   #I'm Not sure about this
        await message.edit("Unspecified Option! Use -p, -v or -g")
        return
    
"""
Will add -t for Texts later on.
"""