from pyroub import *
from pyrogram import filters
from core.database import *
from core.helpers.pyrohelper import get_arg
# from core.helpers.admincheck import CheckAdmin

async def iter_chats(app):
    chats = []
    async for dialog in app.iter_dialog():
        if dialog.chat.type in ["supergroup", "channel"]:
            chats.append(dialog.chat.id)
    return chats
    
@app.on_message(cmd("gban") & filters.user(AUTH))
async def gban(_, message):
    reply =  message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.reply("Give a ID or Username to Gban")
            return
    failed = 0
    get_user = await app.get_users(user)
    chats = await iter_chats(app)
    chat_len = len(chats)
    if not chats:
        message.edit("No Chats Found")
        return
    await message.edit(f"Starting Global Bans of {get_user.mention}!")
    for owo in chats:
        try:
            await app.kick_chat_member(owo, int(get_user.id))
        except:
            failed += 1
    await gban_user(get_user.id)
    await message.edit(f"Gbanned {get_user.mention} in {chat_len-failed} chats!")
    await app.send_message(G_LOG, f"Gbanned {get_user.mention} successfully")
    
@app.on_message(cmd("ungban") & filters.user(AUTH))
async def ungban(_, message):
    reply =  message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.reply("Give an ID or Username to Ungban")
            return
    failed = 0
    get_user = await app.get_users(user)
    chats = await iter_chats(app)
    chat_len = len(chats)
    if not chats:
        message.edit("No Chats Found")
        return
    await message.edit(f"Removing Global Bans of {get_user.mention}!")
    for owo in chats:
        try:
            await app.unban_chat_member(owo, int(get_user.id))
        except:
            failed += 1
    await ungban_user(get_user.id)
    await message.edit(f"Ungbanned {get_user.mention} in {chat_len-failed} chats!")
    await app.send_message(G_LOG, f"Ungbanned {get_user.mention} successfully")
    
@app.on_message(cmd("gmute") & filters.user(AUTH))
async def gmuth(_, message):
    is_reply = message.reply_to_message
    if is_reply:
        user = is_reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.reply("Donate an ID or Username to Gmute!")
    get_user = await app.get_users(user)
    await gmute_user(get_user.id)
    await message.edit(f"Gmuted {get_user.mention}!")
    await app.send_message(G_LOG, f"Gmuted {get_user.mention}!")
    
@app.on_message(cmd("ungmute") & filters.user(AUTH))
async def ungmuth(_, message):
    is_reply = message.reply_to_message
    if is_reply:
        user = is_reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.reply("Donate an ID or Username to Ungmute!")
    get_user = await app.get_users(user)
    await ungmute_user(get_user.id)
    await message.edit(f"Ungmuted {get_user.mention}!")
    await app.send_message(G_LOG, f"Ungmuted {get_user.mention}!")

@app.on_message(filters.group & filters.incoming)
async def check_and_ban(_, message):
    if not message:
        return
    if not message.from_user:
        return
    try:
        if not message.from_user.id in (await get_gbanned_user()):
            return
    except:
        return
    user = message.from_user["id"]
    try:
        admeme = await message.chat.get_member(int(app.me.id))
    except:
        return
    if not admeme.can_restrict_member:
        await message.reply("@admins\nThis user is currently Gbanned in my userbot for active Spamming! Mind muting or Banning this user.")
        return
    try:
        await app.kick_chat_member(message.chat.id, int(user))
        eww = await app.get_users(user)
        await app.send_message(message.chat.id, f"Gbanned User Spotted: {eww.mention}\nSuccessfully Banned!")
    except:
        return
    
@app.on_message(filters.group & filters.incoming)
async def check_and_delete(_, message):
    if not message:
        return
    try:
        if not message.from_user.id in (await get_gmuted_user()):
            return
    except:
        return
    msg = message.message_id
    try:
        await app.delete_message(message.chat.id, msg)
    except:
        pass