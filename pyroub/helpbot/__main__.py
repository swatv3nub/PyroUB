from pyroub import *
from pyrogram import filters

@bot.on_message(bot_cmd(["start", f"start@{BOT_USERNAME}"]) & ~filters.edited & ~filters.me)
async def start(_, message):
	if message.chat.type != "private":
		if message.from_user.id in AUTH:
			await message.reply("Hello! I am your Personal Assistant Bot.")
		else:
			await message.reply("I reply to Sudo Users Only!")
	else:
		if message.from_user.id not in AUTH:
			await bot.send_message(message.chat.id, "Hello! I don't handle commands from strangers, sorry!")
			return

		await bot.send_message(message.chat.id, "Coming Soon Master!")
