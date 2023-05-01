from pyroub import *
from pyrogram import filters
from core.helpers.checkaddon import CheckSelfInstaller

@app.on_command(cmd("install") & filters.me)
async def install(_, message):
    if CheckSelfInstaller() is False:
        await eor(message, f"Self Installer is off. Enable it by running `{PREFIX}var -s SELF_INSTALLER ENABLE` (if you're using Heroku) else edit your config.py file")
        return
    if os.path.exists("sample_config.py"):
        await eor(message, "Availabe for SelfHost only as of now!")
        return
    if not message.reply_to_message:
        await eor(message, "Reply to a Plugin!")
        return
    if not message.reply_to_message.document:
        await eor(message, "Reply to a Plugin!")
        return
    file = message.reply_to_message.document.file_name
    is_py = file.split(".")[1]
    if is_py.lower() != "py":
        await eor(message, "Only Python Files Allowed!")
        return
    if os.path.exists(os.path.join("pyroub/modules/" + file)):
        await eor(message, "Plugin Already Installed!")
        return
    await message.reply_to_message.download(file_name="pyroub/modules/")
    await eor(message, f"Installed {file}\nRestart once!")
    return
    