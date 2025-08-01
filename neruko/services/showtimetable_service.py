import requests
import time
import tldextract
from neruko.models import showtimetable
from urllib.parse import urlparse
    
def insert_showlog(title, startTime, endTime, location):
    updateTime = int(time.time() * 1000)  # 毫秒时间戳
    
    """插入演出记录"""
    try:
        res = showtimetable.insert_showlog(title, startTime, endTime, location, updateTime)
        return res, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
def find_all_showlog():
    """获取 全部演出记录"""
    try:
        res = showtimetable.find_all()
        return res, 200
    except Exception as e:
        return {"error": str(e)}, 500