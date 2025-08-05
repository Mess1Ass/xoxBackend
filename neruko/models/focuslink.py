from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.db_util import get_collection
import datetime
import time


collection = get_collection("FocusLinks")

# link结构:[{url, label}]

# 插入直拍记录
def insert_folink(date, title, links):
    result = collection.insert_one({
        "date": date,
        "title": title,
        "links": links,
        "updateTime": int(time.time() * 1000)
    })
    return result.inserted_id


def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])  # ObjectId -> str
    return doc

# 查看全部直拍
def find_all():
    return [serialize_doc(doc) for doc in collection.find()]

# 根据日期和标题查找记录
def find_by_date_and_title(date, title):
    return collection.find_one({"date": date, "title": title})

# 根据id更新记录
def update_folink(_id, date, title, links):
    result = collection.update_one(
        {"_id": ObjectId(_id)},
        {"$set": {
            "date": date,
            "title": title,
            "links": links,
            "updateTime": int(time.time() * 1000)
        }},
        upsert=True
    )
    return result.modified_count > 0  # True 表示更新成功

# 根据id删除记录
def delete_folink(_id):
    return collection.delete_one({"_id": ObjectId(_id)})




