import asyncio
from pyroub import mongo

gbandb = mongo["pyroub"]["globalban"]
gmutedb = mongo["pyroub"]["globalmute"]
afkdb = mongo["pyroub"]["afk"]
pmguarddb = mongo["pyroub"]["pmguard"]

#gban

async def gban_user(chat):
    data = {"uid": "Gban", "users": [chat]}
    x = await gbandb.find_one({"uid": "Gban"})
    if x:
        await gbandb.update_one({"uid": "Gban"}, {"$push": {"users": chat}})
    else:
        await gbandb.insert_one(data)
    
async def ungban_user(chat):
    await gbandb.update_one({"uid": "Gban"}, {"$pull": {"users": chat}})
    
async def get_gbanned_user():
    found = await gbandb.find_one({"uid": "Gban"})
    if found:
        return found["users"]
    else:
        return []
        
#gmute 

async def gmute_user(chat):
    data = {"uid": "Gmute", "users": [chat]}
    x = await gmutedb.find_one({"uid": "Gmute"})
    if x:
        await gmutedb.update_one({"uid": "Gmute"}, {"$push": {"users": chat}})
    else:
        await gmutedb.insert_one(data)
    
async def ungmute_user(chat):
    await gmutedb.update_one({"uid": "Gmute"}, {"$pull": {"users": chat}})
    
async def get_gmuted_user():
    found = await gmutedb.find_one({"uid": "Gmute")
    if found:
        return found["users"]
    else:
        return []
        
#afk

async def set_afk(afk_status, afk_since, reason):
    data = {"uid": 1, "afk_status": afk_status}
    x = await afkdb.find_one({"uid": 1,})
    if x:
        await afkdb.update_one(
            {"uid": 1},
            {
                "$set": {
                    "afk_status": afk_status,
                    "afk_since": akf_since,
                    "reason": reason,
                }
            },
        )
    else:
        await afkdb.insert_one(data)
        
async def remove_afk_status():
    await afkdb.update_one(
        {"uid": 1}, {"$set": {"afk_status": False, "afk_since": None, "reason": None}}
    )
    
async def get_afk_status():
    is_afk = await afkdb.find_one({"uid": 1})
    if is_afk:
        res = afk["akf_status"]
        return res
    else:
        return False
    
async def afk_detail():
    res = await afkdb.find_one({"uid": 1})
    afk_since = res["afk_since"]
    reason = res["reason"]
    return afk_since, reason
    
#pmguard

PMGUARD_MESSAGE = "I'm a using an userbot in order to protect my PM from any kind of Spam. Please Wait for Me to come and Check Your Message. Until then, don't spam my PM, Or you'll get blocked and reported!"

BLOCKED = "Spammer Spotted! Successfully Blocked and Reported as Spam."

LIMIT = 5

async def set_pm(value: bool):
    doc = {"_id": 1, "pmguard": value}
    doc2 = {"_id": "Approved", "users": []}
    r = await pmguarddb.find_one({"_id": 1})
    r2 = await pmguarddb.find_one({"_id": "Approved"})
    if r:
        await pmguarddb.update_one({"_id": 1}, {"$set": {"pmguard": value}})
    else:
        await pmguarddb.insert_one(doc)
    if not r2:
        await pmguarddb.insert_one(doc2)

async def set_permit_message(text):
    await pmguarddb.update_one({"_id": 1}, {"$set": {"pmguard_message": text}})

async def set_block_message(text):
    await pmguarddb.update_one({"_id": 1}, {"$set": {"block_message": text}})

async def set_limit(limit):
    await pmguarddb.update_one({"_id": 1}, {"$set": {"limit": limit}})

async def get_pm_settings():
    result = await pmguarddb.find_one({"_id": 1})
    if not result:
        return False
    pmguard = result["pmguard"]
    pm_message = result.get("pmguard_message", PMGUARD_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmguard, pm_message, limit, block_message

async def allow_user(chat):
    doc = {"_id": "Approved", "users": [chat]}
    r = await pmguarddb.find_one({"_id": "Approved"})
    if r:
        await pmguarddb.update_one({"_id": "Approved"}, {"$push": {"users": chat}})
    else:
        await pmguarddb.insert_one(doc)

async def get_approved_users():
    results = await pmguarddb.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []

async def deny_user(chat):
    await pmguarddb.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})

async def pm_guard():
    result = await pmguarddb.find_one({"_id": 1})
    if not result:
        return False
    if not result["pmguard"]:
        return False
    else:
        return True
