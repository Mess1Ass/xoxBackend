from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.db_util import get_collection
import datetime



nerukoCollection = get_collection("IpLogs", db_name="Neruko")

def insert_iplog(ip, timestamp_ms, location, domain):
    result = nerukoCollection.insert_one({
        "ip": ip,
        "timestamp_ms": timestamp_ms,
        "location": location,
        "domain": domain
    })
    return result


def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])  # ObjectId -> str
    return doc

# 查看全部直拍
def find_all():
    return [serialize_doc(doc) for doc in nerukoCollection.find()]

# 获取指定域名的访问次数
def get_iplog_cnt(domain):
    return nerukoCollection.count_documents({'domain': domain})


# 根据日期和标题查找记录
def find_by_date_and_title(date, title):
    return nerukoCollection.find_one({"date": date, "title": title})

# 根据id更新记录
def update_iplog(_id, date, title, links):
    result = nerukoCollection.update_one(
        {"_id": ObjectId(_id)},
        {"$set": {
            "date": date,
            "title": title,
            "links": links
        }},
        upsert=True
    )
    return result.modified_count > 0  # True 表示更新成功

# 根据id删除记录
def delete_iplog(_id):
    return nerukoCollection.delete_one({"_id": ObjectId(_id)})