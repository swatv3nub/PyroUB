import os
import sys
import signal
import requests
import wikipedia
import pyshorteners
from tswift import Song
from pyroub import *
from textblob import TextBlob
from pyrogram import filters
from core.helpers.pyrohelper import *

@app.on_message(cmd("chat") & filters.me)
async def chat(_, message):
    try:
        arg = message.text.split()[1]
    except IndexError:
        await eor(message, "Give an argument. -j to join, -l to leave")
        return
    if arg.lower() == "-j":
        try:
            chat = message.text.split()[2]
        except IndexError:
            await eor(message, "Join Where, Give a Username or Link")
            return
        try:
            await app.join_chat(chat)
        except BaseException as e:
            await eor(message, f"Error:\n{e}")
            return
        await eor(message, "Joined the Given Chat!")
        await app.send_message(LOG_CHAT, f"Joined Chat {chat}")
    elif arg.lower() == "-l":
        try:
            chat = message.text.split()[2]
        except IndexError:
            chat = message.chat.id
        await message.delete()
        try:
            await app.leave_chat(chat)
        except BaseException as e:
            await eor(message, f"Error:\n{e}")
            return
        await app.send_message(LOG_CHAT, f"Left Chat: {chat}")
    else:
        await eor(message, "Something went wrong. Use proper Arguments!")
        return

@app.on_message(cmd("invite") & filters.user(AUTH) & ~filters.private)
async def invite(_, message):
    arg = get_arg(message)
    if not arg:
        await eor(message,"Give an Username to Invite")
        return
    user = await app.get_user(arg)
    try:
        await app.add_chat_member(message.chat.id, user.id)
    except Exception as e:
        await eor(message, f"Error:\n{e}")
        return
    await eor(message, f"Added {user.mention} to this chat!")
        
@app.on_message(cmd("ip") & filters.user(AUTH))
async def ip(_, message):
    try:
        arg = message.text.split()[1]
    except IndexError:
        await eor(message, "Give a Argument -me or -ip [ip]")
        return
    if arg.lower() == "-ip":
        try:
            ip = message.text.split(" ", 2)[2]
        except IndexError:
            await eor(message, "Give a IP Address or use arg -me to check your IP!")
            return
        url = requests.get(f"http://ip-api.com/json{ip}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query")
        response = json.loads(url.text)
        text = f"""
**IP Address:** `{response['query']}`
**Status:** `{response['status']}`
**Continent Code:** `{response['continentCode']}`
**Country:** `{response['country']}`
**Country Code :** `{response['countryCode']}`
**Region:** `{response['region']}`
**Region Name :** `{response['regionName']}`
**City:** `{response['city']}`
**District:** `{response['district']}`
**ZIP:** `{response['zip']}`
**Latitude:** `{response['lat']}`
**Longitude:** `{response['lon']}`
**Time Zone:** `{response['timezone']}`
**Offset:** `{response['offset']}`
**Currency:** `{response['currency']}`
**ISP:** `{response['isp']}`
**Org:** `{response['org']}`
**As:** `{response['as']}`
**Asname:** `{response['asname']}`
**Reverse:** `{response['reverse']}`
**User is on Mobile:** `{response['mobile']}`
**Proxy:** `{response['proxy']}`
**Hosting:** `{response['hosting']}`"""
        try:
            await eor(message, text, parse_mode="markdown")
        except BaseException:
            await eor(message, "Error: Unable to Find Info!")
            return
    elif arg.lower() == "-me":
        url = "https://ipinfo.io/ip"
        text = requests.get(url).text
        await eor(message, f"Your IP\n{text}")
    else:
        await eor(message, "Argument not Specified use -me or -ip [ip]")
        
@app.on_message(cmd("change") & filters.me)
async def change_name(_, message):
    try:
        arg = message.text.split()[1]
    except IndexError:
        await eor(message, "Give a Argument -fn, -ln, -un or -bio")
        return
    try:
        name = message.text.split(" ", 2)[2]
        if len(name) > 64:
            await eor(message, "Max Characters: 64")
            return
    except IndexError:
        await eor(message, "Give a Name too")
        return
    if arg.lower() == "-fn":
        try:
            await app.update_profile(first_name=name)
        except BaseException as be:
            await eor(message, f"Error:\n{be}")
            return
        await eor(message, f"Changed FirstName to {name}")
    elif arg.lower == "-ln":
        try:
            await app.update_profile(last_name=name)
        except BaseException as be:
            await eor(message, f"Error:\n{be}")
            return
        await eor(message, f"Changed LastName to {name}")
    elif arg.lower() == "-un":
        try:
            await app.update_username(name)
        except BaseException as be:
            await eor(message, f"Error:\n{be}")
            return
        await eor(message, f"Changed Username to {name}")
    elif arg.lower() == "-bio":
        try:
            bio = message.text.split(" ", 2)[2]
            if len(bio) > 70:
                await eor(message, "Max Limit: 70")
                return
        except IndexError:
            await eor(message, "What to Update in Bio?")
            return
        try:
            await app.update_profile(bio=bio)
        except BaseException as be:
            await eor(message, f"Error\n{be}")
            return
        await eor(message, f"Changed Bio to {bio}")
    else:
        await eor(message, "Argument Not Specified. Use -fn, -ln, -un or -bio!")
        return
    
@app.on_message(cmd("pm") & filters.me)
async def pm(_, message):
    try:
        x = message.text.split()[1]
    except IndexError:
        await eor(message, "Give a Username or ID!")
        return
    try:
        msg = message.text.split(" ", 2)[2]
    except IndexError:
        await eor(message, "Where is the message?")
        return
    user = await app.get_users(x)
    try:
        await app.send_message(user.id, msg)
    except Exception as e:
        await eor(message, f"Error:\n{e}")
        return
    
@app.on_message(cmd(["wiki", "wikipedia"]) & filters.user(AUTH))
async def wiki(_, message):
    query = get_arg(message)
    if not query:
        await eor(message, "What to Search in Wikipedia!")
        return
    resp = wikipedia.search(query)
    rp = ""
    for x in resp:
        try:
            page = wikipedia.page(x)
            url = page.url
            rp += f"• [{x}]({url})\n"
        except BaseException:
            pass
    await eor(message, f"Wiki Search: {query}\nResult: {rp}", disable_web_page_preview=True)
    
@app.on_message(cmd("spcheck") & filters.user(AUTH))
async def spell_check(_, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            query = message.reply_to_message.text
        elif message.reply_to_message.caption:
            query = message.reply_to_message.caption
        else:
            await eor(message, "Reply to a Message with Texts!")
            return
    else:
        query = get_arg(message)
    if not query:
        await eor(message, "Give Some words to check its Spelling")
        return
    check = TextBlob(query)
    correct = check.correct()
    reply = f"Given Phrase/Word: {query}\nCorrected: {correct}"
    if len(reply) > 1024:
        file = "./DOWNLOADS/spellcheck.txt"
        if os.path.exists(file):
            os.remove(file)
        open(file, "w").write(reply)
        await app.send_document(message.chat.id, file, caption="Result of Spelling Check!")
        await message.delete()
        os.remove(file)
    else:
        await eor(message, reply)
        
@app.on_message(cmd("url") & filters.user(AUTH)) # -s / -l
async def url_tool(_, message):
    api = pyshorteners.Shortener()
    try:
        arg = message.text.split()[1]
    except IndexError:
        await eor(message, "Give a Argumnent. -s or -l")
        return
    try:
        url = message.text.split(" ", 2)[2]
    except IndexError:
        await eor(message, "Where is the URL?")
        return
    if arg.lower() == "-s":
        res = api.tinyurl.short(url)
        typ = "Shortened"
    elif arg.lower() == "-l":
        if not "tinyurl.com" in url.lower():
            await eor(message, "Can Expand a Tinyurl URL Only!")
            return
        res = api.tinyurl.expand(url)
        typ = "Expanded"
    else:
        await eor(message, "Argumnent not Specified. Use -s or -l.")
        return
    await eor(message, f"Given URL: {url}\nOutput: {res}\nType: {typ}")
    
@app.on_message(cmd("github") & filters.user(AUTH))
async def git(_, message):
    u_URL = f"https://api.github.com/users/{query}"
    r_URL = "" #Soon
    try:
        arg = message.text.split()[1]
    except IndexError:
        await eor(message, "Give an argument, -u or -r")
        return
    if arg.lower() == "-u":
        try:
            query = message.text.split(" ", 2)[2]
        except IndexError:
            await eor(message, "Give an Github user name too")
            return
        try:
            res = requests.get(u_URL)
        except BaseException as e:
            await eor(message, f"Error:\n{e}")
            return
        result = f"""
**Info of {res['name']}**
**Username:** {query}
**Bio:** {res['bio']}
**Profile:** [Link]({res['html_url']})
**Company:** {res['company']}
**Public Repos:** {res['public_repos']}
**Blog:** {res['blog']}
**Location:** {res['location']}
**Followers:** {res['followers']}
**Following:** {res['following']}
"""
        await eor(message, result)
        
    elif arg.lower() == "-r":
        """
        try:
            query = message.text.split(" ", 2)[2]
        except IndexError:
            await eor(message, f"Give Repo link with username and Repo name Only:\nEg: {PREFIX}github -r swatv3nub/PyroUB")
            return
        """
        await eor(message, "URL Giving Unknown Errors! will fix soon")
        return
    else:
        await eor(message, "Unknown Argument!")
        
@app.on_message(cmd(["restart", "reboot"]) & filters.user(AUTH))
async def reboot(_, message):
    await eor(message, "Rebooting...")
    os.execvp(sys.executable, "-m", "pyroub")

@app.on_message(cmd(["shutdown", "kill"]) & filters.me)
async def sd(_, message):
    await eor(message, "Shutting Down...")
    os.kill(os.getpid(), signal.SIGINT)