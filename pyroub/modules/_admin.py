import asyncio

from core.helpers.admincheck import *
from core.helpers.pyrohelper import *
from pyrogram import filters
from pyrogram.errors import UserAdminInvalid
from pyrogram.methods.chats.get_chat_members import Filters
from pyrogram.types import ChatPermissions, Message
from pyroub import *


@app.on_message(cmd("ban") & filters.me)
async def ban_hammer(_, message):
    if await CheckBanPerms(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await eor(message, "**I can't ban no-one, can I?**")
                return
        try:
            get_user = await app.get_users(user)
            await app.kick_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await eor(message, f"Banned {get_user.first_name} from the chat.")
        except:
            await eor(message, "**I can't ban this user.**")
    else:
        await eor(message, "**Am I an admin here?**")


@app.on_message(cmd("unban") & filters.me)
async def unban(_, message):
    if await CheckBanPerms(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await eor(message, "**I need someone to be unbanned here.**")
                return
        try:
            get_user = await app.get_users(user)
            await app.unban_chat_member(chat_id=message.chat.id, user_id=get_user.id)
            await eor(message, f"Unbanned {get_user.first_name} from the chat.")
        except:
            await eor(message, "**I can't unban this user.**")
    else:
        await eor(message, "**Am I an admin here?**")


# Mute Permissions
mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_stickers=False,
    can_send_animations=False,
    can_send_games=False,
    can_use_inline_bots=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@app.on_message(cmd("mute") & filters.me)
async def mute_hammer(_, message):
    if await CheckBanPerms(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await eor(message, "****I can't mute no-one, can I?**")
                return
        try:
            get_user = await app.get_users(user)
            await app.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
                permissions=mute_permission,
            )
            await eor(message, f"{get_user.first_name} has been muted.")
        except:
            await eor(message, "**I can't mute this user.**")
    else:
        await eor(message, "**Am I an admin here?**")


# Unmute permissions
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_stickers=True,
    can_send_animations=True,
    can_send_games=True,
    can_use_inline_bots=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@app.on_message(cmd("unmute") & filters.me)
async def unmute(_, message):
    if await CheckBanPerms(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await eor(message, "**Whome should I unmute?**")
                return
        try:
            get_user = await app.get_users(user)
            await app.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
                permissions=unmute_permissions,
            )
            await eor(message, f"{get_user.first_name} was unmuted.")
        except:
            await eor(message, "**I can't unmute this user.**")
    else:
        await eor(message, "**Am I an admin here?**")


@app.on_message(cmd("kick") & filters.me)
async def kick_user(_, message):
    if await CheckBanPerms(message) is True:
        reply = message.reply_to_message
        if reply:
            user = reply.from_user["id"]
        else:
            user = get_arg(message)
            if not user:
                await eor(message, "**Whome should I kick?**")
                return
        try:
            get_user = await app.get_users(user)
            await app.kick_chat_member(
                chat_id=message.chat.id,
                user_id=get_user.id,
            )
            await app.unban_chat_member(
                chat=message.chat.id,
                user_id=get_user.id,
            )
            await eor(message, f"Kicked {get_user.first_name} from the chat.")
        except:
            await eor(message, "**I can't kick this user.**")
    else:
        await eor(message, "**Am I an admin here?**")


@app.on_message(cmd("pin") & filters.me)
async def pin_message(_, message):
    if message.chat.type in ["group", "supergroup"]:
        admins = await app.get_chat_members(
            message.chat.id, filter=Filters.ADMINISTRATORS
        )
        admin_ids = [user.user.id for user in admins]
        me = await app.get_me()
        if me.id in admin_ids:
            if message.reply_to_message:
                disable_notification = True
                if len(message.command) >= 2 and message.command[1] in [
                    "alert",
                    "notify",
                    "loud",
                ]:
                    disable_notification = False
                await app.pin_chat_message(
                    message.chat.id,
                    message.reply_to_message.message_id,
                    disable_notification=disable_notification,
                )
                await eor(message, "`Pinned message!`")
            else:
                await eor(message, 
                    "Reply to a message so that I can pin it"
                )
        else:
            await eor(message, "`I am not an admin here lmao. What am I doing?`")
    else:
        await eor(message, "`This is not a place where I can pin shit.`")
    await asyncio.sleep(3)
    await message.delete()


@app.on_message(cmd("promote") & filters.me)
async def promote(client, message):
    if await CheckBanPerms(message) is False:
        await eor(message, "**Am I an admin here?.**")
        return
    title = ""
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
        try:
            title = str(message.text.split()[1])
        except IndexError:
            title = "admin"
    else:
        args = get_args(message)
        if not args:
            await eor(message, "**I can't promote no-one, can I?**")
            return
        user = args[0]
        if len(args) > 1:
            title = " ".join(args[1:])
    get_user = await app.get_users(user)
    try:
        await app.promote_chat_member(message.chat.id, user, can_pin_messages=True)
        await eor(message, 
            f"**{get_user.mention} is now powered with admin rights with {title} as title!**"
        )
    except Exception as e:
        await eor(message, f"{e}")
    if title:
        try:
            await app.set_administrator_title(message.chat.id, user, title)
        except:
            pass


@app.on_message(cmd("allrights") & filters.me)
async def allrights(client, message):
    if await CheckOwner(message) is False:
        await eor(message, "Group Owner only Command!")
        return
    title = ""
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
        title = str(get_arg(message))
    else:
        args = get_args(message)
        if not args:
            await eor(message, "**I can't promote no-one, can I?**")
            return
        user = args[0]
        if len(args) > 1:
            title = " ".join(args[1:])
    get_user = await app.get_users(user)
    try:
        await app.promote_chat_member(
            message.chat.id,
            user,
            is_anonymous=False,
            can_change_info=True,
            can_delete_messages=True,
            can_edit_messages=True,
            can_invite_users=True,
            can_promote_members=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_post_messages=True,
        )
        await eor(message, 
            f"**{get_user.first_name} is now an SuperAdmin with {title} title**"
        )
    except Exception as e:
        await eor(message, f"{e}")
    if title:
        try:
            await app.set_administrator_title(message.chat.id, user, title)
        except:
            pass


@app.on_message(cmd("demote") & filters.me)
async def demote(client, message):
    if await CheckBanPerms(message) is False:
        await eor(message, "**I am not admin.**")
        return
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await eor(message, "**I can't demote no-one, can I?**")
            return
    get_user = await app.get_users(user)
    try:
        await app.promote_chat_member(
            message.chat.id,
            user,
            is_anonymous=False,
            can_change_info=False,
            can_delete_messages=False,
            can_edit_messages=False,
            can_invite_users=False,
            can_promote_members=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_post_messages=False,
        )
        await eor(message, 
            f"**{get_user.first_name} is now stripped off of their admin rights!**"
        )
    except Exception as e:
        await eor(message, f"{e}")


@app.on_message(cmd("invite") & filters.me & ~filters.private)
async def invite(client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await eor(message, "**I can't invite no-one, can I?**")
            return
    get_user = await app.get_users(user)
    try:
        await app.add_chat_members(message.chat.id, get_user.id)
        await eor(message, f"**Added {get_user.first_name} to the chat!**")
    except Exception as e:
        await eor(message, f"{e}")
