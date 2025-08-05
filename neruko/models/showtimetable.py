from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.db_util import get_collection
import datetime



collection = get_collection("ShowTimeTable")

def insert_showlog(title, startTime, endTime, location, updateTime):
    result = collection.insert_one({
        "title": title,
        "startTime": startTime,
        "endTime": endTime,
        "location": location,
        "updateTime": updateTime
    })
    return result.inserted_id


def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])  # ObjectId -> str
    return doc

# 查看全部时间表
def find_all():
    return [serialize_doc(doc) for doc in collection.find()]


def find_earliest_showlog(today):
    doc = collection.find_one(
        {"startTime": {"$gt": today}},
        sort=[("startTime", 1)]  # 升序排序，离今天最近
    )
    return serialize_doc(doc)


# 根据日期和标题查找记录
def find_by_id(_id):
    return collection.find_one({"_id": ObjectId(_id)})

# 根据id更新记录
def update_showlog(_id, title, startTime, endTime, location, updateTime):
    result = collection.update_one(
        {"_id": ObjectId(_id)},
        {"$set": {
            "title": title,
            "startTime": startTime,
            "endTime": endTime,
            "location": location,
            "updateTime": updateTime
        }},
        upsert=True
    )
    return result.modified_count > 0  # True 表示更新成功

# 根据id删除记录
def delete_showlog(_id):
    return collection.delete_one({"_id": ObjectId(_id)})