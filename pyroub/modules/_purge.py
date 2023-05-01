import math
import asyncio
from datetime import datetime
from pyroub import *
from pyrogram.types import Message
from core.helpers.admincheck import CheckDelPerms

@app.on_message(cmd("purge") & filters.user(AUTH) & ~filters.private)
async def purge_message(_, message):
    if message.chat.type in (("supergroup", "channel")):
        if await CheckDelPerms(message) is False:
            await message.delete()
            return
    else:
        pass
    start_t = datetime.now()
    await message.delete()
    message_ids = []
    del_msgs = 0
    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.message_id, message.message_id
        ):
            message_ids.append(a_s_message_id)
            if len(message_ids) == 100:
                await app.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                del_msgs += len(message_ids)
                message_ids = []
        if message_ids:
            await app.delete_messages(
                chat_id=message.chat.id, message_ids=message_ids, revoke=True
            )
            del_msgs += len(message_ids)
    end_t = datetime.now()
    time_taken_ms = (end_t - start_t).seconds
    msg = await app.send_message(
        message.chat.id,
        f"Purged {del_msgs} messages in {time_taken_ms} seconds",
    )
    await asyncio.sleep(5)
    await msg.delete()

@app.on_message(cmd("del") & filters.user(AUTH))
async def delete_replied(_, message):
    if not message.reply_to_message:
        await eor(message, "Reply to a Message to Delete!")
        return
    try:
        await message.reply_to_message.delete()
        await message.delete()
    except Exception as e:
        await eor(message, f"Error:\n{e}")
