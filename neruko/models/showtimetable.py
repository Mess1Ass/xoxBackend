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
    return result


def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])  # ObjectId -> str
    return doc

# 查看全部时间表
def find_all():
    return [serialize_doc(doc) for doc in collection.find()]

# 获取指定域名的访问次数
def get_iplog_cnt(domain):
    return collection.count_documents({'domain': domain})


# 根据日期和标题查找记录
def find_by_date_and_title(date, title):
    return collection.find_one({"date": date, "title": title})

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
def delete_iplog(_id):
    return collection.delete_one({"_id": ObjectId(_id)})