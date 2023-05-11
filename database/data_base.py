from vars import DB_URI, DB_NAME, COLLECTION_NAME, TARGET_DB
from pymongo import MongoClient

client = MongoClient(DB_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

async def add_user(userid, username, name):
    user_details = {
        "id": int(userid),
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
    user = collection.find_one({'id': int(userid)})
    return bool(user)
    
async def count_users():
    total = await collection.count_documents({})
    return total

def ban_user(userid, reason):
    collection.update_one({'id': int(userid)}, {'$set': {'is_banned': True, 'ban_reason': reason}})

def unban_user(userid):
    collection.update_one({'id': int(userid)}, {'$set': {'is_banned': False, 'ban_reason': None}})

async def get_all_users():
    return collection.find({})

async def get_user(userid):
    user = await collection.find_one({'id': int(userid)})
    return user
    
def update_stats(userid, msgid, last_msg_id, sourcechat, target, on_process):
    collection.update_one(
        {'id': int(userid)},
        {'$set': {'target': target, 'source': sourcechat, 'skip': msgid, 'last_msg_id': last_msg_id, 'on_process': on_process}},
        upsert=True
    )

def update_target(userid, target):
    collection.update_one(
        {'id': int(userid)},
        {'$set': {'target': target}}
    )

def update_caption(userid, caption):
    collection.update_one(
        {'id': int(userid)},
        {'$set': {'caption': caption}}
    )