import requests
from pyroub import *
from pyrogram import filters

@app.on_message(cmd("aniquote") & filters.user(AUTH))
async def aniquote(_, message):
    try:
        resp = requests.get("https://animechan.vercel.app/api/random").json()
        results = f"**{resp['quote']}**\n"
        results += f" — {resp['character']} ({resp['anime']})"
        await eor(message, results)
        return
    except Exception as e:
        await eor(message, f"Something Went Wrong\nError: {e}")
        return