from vars import DB_URI, DB_NAME, COLLECTION_NAME, TARGET_DB
from pymongo import MongoClient

client = MongoClient(DB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

async def add_user(userid, username, name):
    user_details = {
        "id": userid,
        "username": username,
        "name": name,
        "target": TARGET_DB,
        "source": None,
        "last_msg_id": 0,
        "on_process": False,
        "skip": 0,
        "is_banned": False,
        "ban_reason": None,
        "caption": "<b>{file_name}</b>"
    }
    await collection.insert_one(user_details)

def is_user_exist(userid):
    user = collection.find_one({'id': userid})
    if user:
        return True
    else:
        return False
    
async def count_users():
    total = await collection.count_documents({})
    return total

async def ban_user(userid, reason):
    await collection.update_one({'id': userid}, {'$set': {'is_banned': True, 'ban_reason': reason}})

async def unban_user(userid):
    await collection.update_one({'id': userid}, {'$set': {'is_banned': False, 'ban_reason': None}})

async def get_all_users():
    return await collection.find({})

async def get_user(userid):
    user = await collection.find_one({'id': userid})
    if user:
        return user
    
async def update_stats(userid, msgid, last_msg_id, sourcechat, target):
    await collection.update_one(
        {'id': userid},
        {'$set': {'target': target, 'source': sourcechat, 'skip': msgid, 'last_msg_id': last_msg_id, 'on_process': True}},
        upsert=True
    )

def update_target(userid, target):
    collection.update_one(
        {'id': userid},
        {'$set': {'target': target}}
    )

async def update_caption(userid, caption):
    await collection.update_one(
        {'id': userid},
        {'$set': {'caption': caption}}
    )