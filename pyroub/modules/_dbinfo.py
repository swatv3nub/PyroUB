from pyroub import *
from pyrogram import filters

@app.on_message(cmd("dbstats") & filters.user(AUTH))
async def dbstats(_, message):
    x = db.pyroub
    owo = x.command("dbstats")
    if "fsTotalSize" in owo:
        msg = f"Database Stats:\nUsed Space: {convert_size(owo["dataSize"])}\nFree Space: {convert_size(owo["fsTotalSize"] - owo["fsUsedSize"])}"
    else:
        msg = f"Database Stats:\nUsed Space: {convert_size(owo["storageSize"])}\nFree Space: {convert_size(536870912 - owo["storageSize"])}"
    await eor(message, msg)
    return
