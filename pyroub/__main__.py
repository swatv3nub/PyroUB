import asyncio

from pyrogram import idle

from pyroub import app, bot, loop, session

if not bot:
    app.run()
    
else:
    async def run():
        await asyncio.gather(app.start(), bot.start())
        await idle()
        await asyncio.gather(app.stop(), bot.stop())
        await session.close()
        
    loop.run_until_complete(run())
