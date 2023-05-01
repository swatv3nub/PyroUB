import asyncio
import os

from core.helpers.pyrohelper import get_arg
from pyrogram import filters
from pyroub import *


@app.on_message(cmd("ghosts") & filters.user(AUTH))
async def delacc(_, message):
    try:
        opt = get_arg(message)
    except:
        await eor(message, "Give an Option for ghost command, -c or -c -d")
        return
    if opt.lower() == "-c -d":
        await eor(message, "Counting Deleted Accounts...")
        del_accs = []
        u = 0
        async for x in app.iter_chat_member(chat_id=message.chat.id):
            for x.user.is_deleted:
                del_accs.append(x.user.id)
        if del_accs:
            await eor(message, f"Found {len(del_accs)} Deleted Accounts! Deleting them as Specified")
        else:
            await eor(message, "No Deleted Accounts Found!")
            return
        async for x in app.iter_chat_member(chat_id=message.chat.id):
            await asyncio.sleep(0.1)
            if x.user.is_deleted:
                del_accs.append(x.user.id)
                c = await app.get_chat_member(message.chat.id, x.user.id)
                if a.user.status not in ("administrator", "creator"):
                    try:
                        await app.kick_chat_member(message.chat.id, x.user.id)
                        u += 1
                        await asyncio.sleep(0.1)
                    except:
                        pass
        await eor(message, f"Group Cleaned!\nRemoved {u} Deleted Accounts")
    elif opt.lower() == "-c":
        await eor(message, "Counting Deleted Accounts...")
        del_accs = []
        u = 0
        async for x in app.iter_chat_member(chat_id=message.chat.id):
            for x.user.is_deleted:
                del_accs.append(x.user.id)
        if del_accs:
            await eor(message, f"Found {len(del_accs)} Deleted Accounts! Deleting them as Specified")
        else:
            await eor(message, "No Deleted Accounts Found!")
            return
    elif opt.lower() == "-d":
        del_accs = []
        u = 0
        async for x in app.iter_chat_member(chat_id=message.chat.id):
            await asyncio.sleep(0.1)
            if x.user.is_deleted:
                del_accs.append(x.user.id)
                c = await app.get_chat_member(message.chat.id, x.user.id)
                if a.user.status not in ("administrator", "creator"):
                    try:
                        await app.kick_chat_member(message.chat.id, x.user.id)
                        u += 1
                        await asyncio.sleep(0.1)
                    except:
                        pass
        await eor(message, f"Group Cleaned!\nRemoved {u} Deleted Accounts")
    else:
        await eor(message, "Unspecified Option, Use '-c', '-d' or '-c -d'")
        return
    