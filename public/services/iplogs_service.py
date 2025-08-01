import requests
import time
import tldextract
from public.models import iplogs
from urllib.parse import urlparse



def get_ip_location():

    """获取 IP 地址对应的地理位置（使用 ip-api）"""
    try:
        res = requests.get(f"http://ip-api.com/json/", timeout=5)
        data = res.json()
        if data["status"] == "success":
            return {
                "country": data.get("country"),
                "regionName": data.get("regionName"),
                "city": data.get("city"),
                "isp": data.get("isp"),
                "lat": data.get("lat"),
                "lon": data.get("lon")
            }, 200
        return {"error": data.get("message", "未知错误")}, 500
    except Exception as e:
        return {"error": str(e)}, 500
    
    
def insert_iplog(ip, domain):
    timestamp_ms = int(time.time() * 1000)  # 毫秒时间戳
    location, code = get_ip_location()
    if code != 200:
        return location, code
    
    """插入 IP 地址日志"""
    try:
        iplogs.insert_iplog(ip, timestamp_ms, location, domain)
        return {"message": "日志插入成功"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    
def get_visit_count(domain):
    """获取 IP 地址访问次数"""
    try:
        count = iplogs.get_iplog_cnt(domain)
        return {"count": count}, 200
    except Exception as e:
        return {"error": str(e)}, 500