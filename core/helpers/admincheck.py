import asyncio
from pyrogram.types import Message
from pyroub import app, eor, UB_ID


async def CheckBanPerms(message: Message):
    admin = "administrator"
    creator = "creator"
    ranks = [admin, creator]

    SELF = await app.get_chat_member(
        chat_id=message.chat.id, user_id=UB_ID
    )

    if SELF.status not in ranks:
        x = await eor(message, "I'm not Admin!")
        asyncio.sleep(2)
        await x.delete()

    else:
        if SELF.status is not admin or SELF.can_restrict_members:
            return True
        else:
            x = await eor(message, "No Permissions to restrict Members")
            asyncio.sleep(2)
            await x.delete()
            

async def CheckDelPerms(message: Message):
    admin = "administrator"
    creator = "creator"
    ranks = [admin, creator]

    SELF = await app.get_chat_member(
        chat_id=message.chat.id, user_id=UB_ID
    )

    if SELF.status not in ranks:
        x = await eor(message, "I'm not Admin!")
        asyncio.sleep(2)
        await x.delete()

    else:
        if SELF.status is not admin or SELF.can_delete_messages:
            return True
        else:
            x = await eor(message, "No Permissions to Delete Message!")
            asyncio.sleep(2)
            await x.delete()
            return False

            
async def CheckOwner(message: Message):
    SELF = await app.get_chat_member(
        chat_id=message.chat.id, user_id=UB_ID
    )
    if SELF.status != "creator":
        return False
    else:
        return True
