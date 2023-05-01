#Most parts are Taken from Zect Userbot by Satwik
#I just added some more "masala"

from pyrogram import filters
from pyrogram.raw.functions.account import ReportPeer
import asyncio
from pyrogram.methods import messages
from pyroub import *
from core.helpers.pyrohelper import get_arg, denied_users
from core.database import pmguarddb as db

FLOOD_CTRL = 0
ALLOWED = []
USERS_AND_WARNS = {}


@app.on_message(cmd("pmguard") & filters.me)
async def pmguard(_, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**I only understand on or off**")
        return
    if arg.lower() == "off":
        await db.set_pm(False)
        await message.edit("**PM Guard Deactivated**")
    if arg.lower() == "on":
        await db.set_pm(True)
        await message.edit("**PM Guard Activated**")


@app.on_message(cmd("setlimit") & filters.me)
async def pmguard(_, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Set limit to what?**")
        return
    await db.set_limit(int(arg))
    await message.edit(f"**Limit set to {arg}**")


@app.on_message(cmd("setpmmsg") & filters.me)
async def setpmmsg(_, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**What message to set**")
        return
    if arg.lower() == "default":
        await db.set_permit_message(db.PMGUARD_MESSAGE)
        await message.edit("**Anti_PM message set to default**.")
        return
    await db.set_permit_message(f"`{arg}`")
    await message.edit("**Custom anti-pm message set**")


@app.on_message(cmd("setblockmsg") & filters.me)
async def setpmmsg(_, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**What message to set**")
        return
    if arg.lower() == "default":
        await db.set_block_message(db.BLOCKED)
        await message.edit("**Block message set to default**.")
        return
    await db.set_block_message(f"`{arg}`")
    await message.edit("**Custom block message set**")


@app.on_message(cmd(["allow", "a"]) & filters.me & filters.private)
async def allow(_, message):
    chat_id = message.chat.id
    pmguard, pm_message, limit, block_message = await db.get_pm_settings()
    await db.allow_user(chat_id)
    await message.edit(f"**Allowed [{chat_id}](tg://user?id={chat_id}) to PM Me.**")
    async for message in app.search_messages(
        chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
    ):
        await message.delete()
    USERS_AND_WARNS.update({chat_id: 0})


@app.on_message(cmd(["deny", "d"]) & filters.me & filters.private)
async def deny(_, message):
    chat_id = message.chat.id
    await db.deny_user(chat_id)
    await message.edit(f"**Denied [{chat_id}](tg://user?id={chat_id}) to PM Me.**")


@app.on_message(cmd("block") & filters.me)
async def blc(_, message):
    if message.chat.type != "private":
        if message.reply_to_message:
            if message.from_user:
                user = message.from_user.id
            else:
                await eor(message, "Reply to a User!")
        else:
            try:
                user = get_arg(message)
            except:
                await message.edit("give an id or username to block!")
    else:
        user = message.chat.id
    msg = "`Successfully Blocked and Reported as spam!`"
    await app.send_message(user, msg)
    report = ReportPeer(
                   peer=user,
                   reason="Spamming My Inbox"
                   )
    await app.send(report)
    await app.block_user(user)
    return

@app.on_message(
    filters.private
    & filters.create(denied_users)
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def reply_pm(_, message):
    global FLOOD_CTRL
    pmguard, pm_message, limit, block_message = await db.get_pm_settings()
    user = message.from_user.id
    user_warns = 0 if user not in USERS_AND_WARNS else USERS_AND_WARNS[user]
    if user_warns <= limit - 2:
        user_warns += 1
        USERS_AND_WARNS.update({user: user_warns})
        if not FLOOD_CTRL > 0:
            FLOOD_CTRL += 1
        else:
            FLOOD_CTRL = 0
            return
        async for message in app.search_messages(
            chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
        ):
            await message.delete()
        await message.reply(pm_message, disable_web_page_preview=True)
        return
    await message.reply(block_message, disable_web_page_preview=True)
    report = ReportPeer(
                   peer=message.chat.id,
                   reason="Spamming My Inbox"
                   )
    await app.send(report)
    await app.block_user(message.chat.id)
    USERS_AND_WARNS.update({user: 0})

