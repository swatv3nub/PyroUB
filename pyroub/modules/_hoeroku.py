import os

import heroku3
from pyrogram import filters
from pyroub import *


@app.on_message(cmd("var") & filters.me)
async def hoe_vars(_, message):
    try:
        app_name = HEROKU_APP_NAME
    except:
        await eor(message, "Setup HEROKU_APP_NAME var in Heroku Properly First")
        return
    try:
        key = HEROKU_API_KEY
    except:
        await eor(message, "Setup HEROKU_API_KEY var in Heroku Properly First")
        return
    try:
        opt = message.text.split()[1]
    except IndexError:
        await eor(message, "No Option Specified!")
        return
    try:
        var = message.text.split()[2]
    except IndexError:
        await eor(message, "No Var Specified!")
        return
    if os.path.exists("config.py"):
        await eor(message, "You are on Self Host, Please Change the config.py file yourself")
        return
    
    heroku = heroku3.from_key(key)
    _app = heroku.app(app_name)
    config = _app.config()
    
    if opt.lower() == "-s":
        try:
            val = message.text.split(" ", 3)[3]
        except IndexError:
            await eor(message, "No Value Specified!")
            return
        config[var] = val
        await eor(message, f"Variable {var}'s' value changed to {val}!")
    if opt.lower() == "-d":
        if not var in config:
            await eor(message, f"No Variable named {var} Exists!")
            return
        del config[var]
        await eor(message, f"Variable {var} Deleted!")
    if opt.lower() == "-g":
        if not var in config:
            await eor(message, f"No Variable named {var} Exists!")
            return
        if var in ["SESSION", "VC_SESSION", "MONGO_DB_URI"]:
            await eor(message, "Prohibited!")
            return
        await eor(message, f"Variable: {var}\nValue: {config[var]}")
        
@app.on_message(cmd("logs") & filters.user(AUTH))
async def logs(_, message):
    try:
        app_name = HEROKU_APP_NAME
    except:
        await eor(message, "Setup HEROKU_APP_NAME var in Heroku Properly First")
        return
    try:
        key = HEROKU_API_KEY
    except:
        await eor(message, "Setup HEROKU_API_KEY var in Heroku Properly First")
        return
    if os.path.exists("config.py"):
        await eor(message, "Logs for Self Hosted PyroUB isn't Available Now, Please wait for next Update!")
        return
    heroku = heroku3.from_key(key)
    _app = heroku.app(app_name)
    with open("logs.txt", "w") as x:
        log = _app.get_log()
        x.write(log)
    await app.send_document(message.chat.id, document="logs.txt", caption=f"Logs of {app_name}")
    os.remove("logs.txt")
    await message.delete()
    
    