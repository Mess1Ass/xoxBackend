import requests
import time
import tldextract
from neruko.models import showtimetable
from urllib.parse import urlparse
from datetime import datetime
    
def insert_showlog(title, startTime, endTime, location):
    startTime = int(startTime)
    endTime = int(endTime)

    updateTime = int(time.time() * 1000)  # 毫秒时间戳
    
    """插入演出记录"""
    try:
        res = showtimetable.insert_showlog(title, startTime, endTime, location, updateTime)
        return str(res), 200
    except Exception as e:
        return {"error": str(e)}, 500
    
def find_all_showlog():
    """获取 全部演出记录"""
    try:
        res = showtimetable.find_all()
        return res, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
    
def find_earliest_showlog():
    """获取 data 大于今天，且离今天最近的一条演出记录"""
    today = int(time.time() * 1000)
    try:
        res = showtimetable.find_earliest_showlog(today)
        return res, 200
    except Exception as e:
        return {"error": str(e)}, 500


def update_showlog(_id, title, startTime, endTime, location):
    startTime = int(startTime)
    endTime = int(endTime)

    updateTime = int(time.time() * 1000)  # 毫秒时间戳
    exist = showtimetable.find_by_id(_id)
    if not exist:
        return {"error": "不存在该记录，请刷新页面"}, 400
    try:
        res = showtimetable.update_showlog(_id, title, startTime, endTime, location, updateTime), 200
        return res
    except Exception as e:
        return {"error": str(e)}, 500
    
def delete_showlog(_id):
    try:
        res = showtimetable.delete_showlog(_id), 200
        return res
    except Exception as e:
        return {"error": str(e)}, 500