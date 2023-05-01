import os
from datetime import datetime
from functools import partial

import requests
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls_wrapper import Wrapper


from pyroub import AUTH
from pyroub import eor

config_exists = os.path.exists("config.py")
if config_exists:
    from config import *
else:
    from sample_config import *
    
cmd = partial(filters.command, prefixes=VC_PREFIX)

vc = Client(VC_SESSION, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(vc)
pycalls = Wrapper(pytgcalls, "raw")

VC_ID = 0
VC_DC = 0
VC_MENTION = ""
async def vc_info(vc):
    global VC_ID, VC_DC, VC_MENTION
    VC = await vc.get_me()
    VC_ID = await VC.id
    VC_DC = await VC.dc_id
    VC_MENTION = await VC.mention
    
AUTH = AUTH
if VC_ID not in AUTH:
    AUTH.append(VC_ID)
    
@vc.on_message(cmd("alive") & filters.user(AUTH))
async def alive(_, message):
    await eor(message, "PyroUB Voice Chat is Active")
    
@vc.on_message(cmd("stream") & filters.user(AUTH))
async def stream(_, message):
    txt = message.text.split(" ", 1)
    typ = None
    try:
        song = txt[1]
        typ = "url"
    except IndexError:
        reply = message.reply_to_message
        if reply:
            if reply.audio:
                med = reply.audio
            elif reply.video:
                med = reply.video
            elif reply.voice:
                med = reply.voice
            else:
                await eor(message, "Give a YouTube Link or Reply to a Media")
                return
            song = med.file_name
            typ = "tg"
    if typ == "url":
        if "youtube" not in song and "youtu.be" not in song:
            await eor(message, "Need a YouTube URL to Stream!")
            return
        await eor(message, f"Playing From {song}")
        try:
            await pycalls.stream(message.chat.id, song)
        except Exception as e:
            await eor(f"Error:\n{e}")
    elif typ == "tg":
        await eor(message, "Downloading...")
        song = await reply.download()
        await eor(message, "Playing")
        try:
            await pycalls.stream(message.chat.id, song)
        except Exception as e:
            await eor(f"Error\n{e}")
        os.remove(song)
    else:
        await eor(message, "Give a YouTube Link or Reply to a Media")
        return

@vc.on_message(cmd("pause") & filters.user(AUTH))
async def pause(_, message):
    pycalls.pause(message.chat.id)
    await eor(message, "Paused the Stream!")
    
@vc.on_message(cmd("resume") & filters.user(AUTH))
async def resume(_, message):
    pycalls.resume(message.chat.id)
    await eor(message, "Resumed the Stream!")
    
@vc.on_message(cmd("ping") & filters.user(AUTH))
async def vcping(_, message):
    s = datetime.now()
    await eor(message, "Pong!")
    e = datetime.now()
    pong = (e-s).microseconds / 1000
    await eor(message, f"VC Ping!\n{pong}ms")
    
@vc.on_message(cmd("vc") & filters.user(AUTH))
async def vcinfo(_, message):
    await eor(message, f"PyroUB VC Info!\nVoiceChat Bot: {VC_MENTION}\nVoiceChat ID: {VC_ID}\nVoiceChat Bot DC: {VC_DC}")
    
@vc.on_message(cmd("help") & filters.user(AUTH))
async def helper(_, message):
    help_text = f"""
    {VC_PREFIX}alive - Check Alive Or Not
    {VC_PREFIX}vc - Check VC Info
    {VC_PREFIX}stream - Give a YouTube URL or Reply to a TG File
    {VC_PREFIX}pause - Pause the Stream
    {VC_PREFIX}resume - Resume the Stream
    {VC_PREFIX}vol <0-200> - Set the Volume"""
    await eor(message, help_text)
    
@vc.on_message(cmd("vol") & filters.user(AUTH))
async def setvol(_, message):
    msg = message.text.split(" ", 1)
    try:
        vol = msg[1]
    except IndexError:
        await eor(message, "Give the Volume to set between 0-200")
    try:
        if int(vol[1]) not in range(0, 201):
            await eor("Give Volume between 0-200")
        pytgcalls.change_volume_call(message.chat.id, int(vol[1]))
    except Exception as e:
        await eor(message, f"Error:\n{e}")
