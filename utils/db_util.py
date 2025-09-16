# db_util.py
from pymongo import MongoClient
import config

# 初始化连接（全局只初始化一次）
_client = MongoClient(config.MONGO_URI)
# _db = _client[config.MONGO_DB]

def get_db(name=None):
    """获取 MongoDB 数据库实例"""
    if name:
        return _client[name]
    return _client[config.MONGO_DB]

def get_collection(name=None, db_name=None):
    """
    获取指定集合，支持传数据库名
    :param name: 集合名
    :param db_name: 数据库名，不传则用默认配置
    """
    db = get_db(db_name)
    if name:
        return db[name]
    return db[config.MONGO_COLLECTION]
