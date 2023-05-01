import time
from pyroub import *
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(cmd("check") & filters.me)
async def check(_, message):
    start_time = time.time()
    x = await message.reply_text("Pyrogram Userbot is Alive!\nChecking Uptime, Ping and Info...")
    end_time = time.time()
    ping = round((end_time - start_time) * 1000, 3)
    uptime = get_redable_time((time.time() - StartTime))
    await x.edit_text(f"Pyrogram Userbot is Alive!\nPing: {ping}ms\nUptime: {uptime}!\n\nOwner: {UB_MENTION}\nAssistantBot: {BOT_MENTION}\n\nTotal Authorised Users: {len(AUTH)}!")
    
@app.on_message(cmd("alive") & filters.user(AUTH))
async def alive(_, message):
    await message.reply("PyroUB is Alive!")
    