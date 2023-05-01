import asyncio
import logging
import math
import os
import sys
import time
from functools import partial
from inspect import getfullargspec

import aiohttp
from core.helpers.checkaddon import *
from google_trans_new import google_translator
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pymongo import MongoClient as MC
from pyrogram import Client, errors, filters
from pyrogram.types import Chat, Message, User
from Python_ARQ import ARQ

config_exists = os.path.exists("config.py")
if config_exists:
    from config import *
else:
    from sample_config import *

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

LOGGER = logging.getLogger(__name__)

SPAMWATCH_API = SPAMWATCH_API
if not SPAMWATCH_API:
    LOGGER.WARNING("SpamWatch API Missing!")

PREFIX = PREFIX
HELP_MODE = HELP_MODE
cmd = partial(filters.command, prefixes=PREFIX)
BOT_PREFIX = ["!", "/"]
bot_cmd = partial(filters.command, prefixes=BOT_PREFIX)
StartTime = time.time()
session = aiohttp.ClientSession()
translate = google_translator()
loop = asyncio.get_event_loop()
arq_url = "http://thearq.tech"
arq = ARQ(arq_url, ARQ_X_API, session)

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH)     # Userbot

if not BOT_TOKEN:
    bot = None
    LOGGER.info("Bot Token Missing, BotLess Mode Started!")
    mode = "BotLess"
else:
    bot = Client(bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH) #Assistant
    mode = "WithAssistant"
LOGGER.info(f"Userbot started with Mode: {mode}")
mongo = MongoClient(MONGO_DB_URI) #Motor
db = MC(MONGO_DB_URI)

#Themks Hamker
UB_ID = 0
UB_NAME = ""
UB_USERNAME = ""
UB_MENTION = ""
UB_DC = 0
BOT_ID = 0
BOT_NAME  = ""
BOT_USERNAME = ""
BOT_MENTION = ""
BOT_DC = 0

def get_info(app, bot):
    global UB_ID, UB_NAME, UB_USERNAME, UB_MENTION, UB_DC
    global BOT_ID, BOT_NAME, BOT_USERNAME, BOT_MENTION, BOT_DC
    get_ub = app.get_me()
    get_bot = bot.get_me()
    UB_ID = get_ub.id
    UB_NAME = get_ub.first_name
    UB_USERNAME = get_ub.username
    UB_MENTION = get_ub.mention
    UB_DC = get_ub.dc_id
    BOT_ID = get_bot.id
    BOT_NAME = get_bot.first_name
    BOT_USERNAME = get_bot.username
    BOT_MENTION = get_bot.mention
    BOT_DC = get_bot.dc_id

AUTH = AUTH_USERS
if UB_ID not in AUTH:
    AUTH.append(UB_ID)
    
LOG_CHAT = LOG_CHAT
if not LOG_CHAT:
    LOG_CHAT = UB_ID
    
G_LOG = GLOBAL_LOG_CHAT
if not G_LOG:
    G_LOG = UB_ID
    
async def eor(message: Message, **kwargs):
    func = message.edit if message.from_user.is_self else message.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})
    
def convert_size(size):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
    
async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for app in apps:
                if app != client:
                    try:
                        entity = await app.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = app
                        break
            else:
                entity = await app.get_chat(entity)
                entity_client = app
    return entity, entity_client
    
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time
