import requests
import json
from flask import Response
from urllib.parse import quote


def get_weibo_vedio_detail(weibo_id):
    try:
        url = f"https://weibo.com/ajax/statuses/show"
        params = {
            "id": weibo_id,
            "locale": "zh-CN",
            "isGetLongText": "true"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "Referer": f"https://weibo.com/{weibo_id}",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": "SINAGLOBAL=6304198927605.606.1719551309878; SCF=AsXbLLiI7q5DRDNLgnr2GKXupEFCHWDFuRcWHQgIdEpvZkOzpeubL8bE6SpCDOjsigEUrADxfTwOiuig4KCd-pM.; XSRF-TOKEN=JbEejd1te3KYyPJVrj_GsJAj; _s_tentry=-; Apache=9125271403219.129.1753342665938; ULV=1753342666026:12:2:2:9125271403219.129.1753342665938:1753321022010; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhZ-bS5f9AHTqrpueS_wGvI5JpVF0241hzpeo57eK50; SUB=_2AkMf28nGdcPxrARYm_wVxW3ibIVH-jysDqAwAn7uJhMyAxhp7mw1qSVutBF-XJ4pbS5RRm754h2WI_2OZgidIwCJ; WBPSESS=Dt2hbAUaXfkVprjyrAZT_M6cIVjKvbs-9Qqm-fUgHQTL98ZibCRRo46gFEtensv7C4mO8hTs94IxMusw6-WR9fVWlXFHB-30rRBYxilTyeMOY0c90Pw_cUPEDp04LzBQPOYRwQnbB7MYTIvnUcXNmQ=="
        }

        res = requests.get(url, params=params, headers=headers, timeout=10)

        if res.status_code != 200:
            return {"error": "请求微博接口失败"}, 500

        json_data = res.json()

        result = []

        if "page_info" in json_data and "media_info" in json_data["page_info"]:
            result.append(json_data["page_info"]["media_info"])
        elif "mix_media_info" in json_data and "items" in json_data["mix_media_info"]:
            result = []
            for item in json_data["mix_media_info"]["items"]:
                if "data" in item:
                    result.append(item["data"]["media_info"])
        else:
            return {"error": "未找到媒体信息"}, 404

        return result, 200

    except Exception as e:
        return {"error": str(e)}, 500
    
def get_b23_vedio_detail(weibo_id):
    try:
        url = f"https://weibo.com/ajax/statuses/show"
        params = {
            "id": weibo_id,
            "locale": "zh-CN",
            "isGetLongText": "true"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "Referer": f"https://weibo.com/{weibo_id}",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": "SINAGLOBAL=6304198927605.606.1719551309878; SCF=AsXbLLiI7q5DRDNLgnr2GKXupEFCHWDFuRcWHQgIdEpvZkOzpeubL8bE6SpCDOjsigEUrADxfTwOiuig4KCd-pM.; XSRF-TOKEN=JbEejd1te3KYyPJVrj_GsJAj; _s_tentry=-; Apache=9125271403219.129.1753342665938; ULV=1753342666026:12:2:2:9125271403219.129.1753342665938:1753321022010; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WhZ-bS5f9AHTqrpueS_wGvI5JpVF0241hzpeo57eK50; SUB=_2AkMf28nGdcPxrARYm_wVxW3ibIVH-jysDqAwAn7uJhMyAxhp7mw1qSVutBF-XJ4pbS5RRm754h2WI_2OZgidIwCJ; WBPSESS=Dt2hbAUaXfkVprjyrAZT_M6cIVjKvbs-9Qqm-fUgHQTL98ZibCRRo46gFEtensv7C4mO8hTs94IxMusw6-WR9fVWlXFHB-30rRBYxilTyeMOY0c90Pw_cUPEDp04LzBQPOYRwQnbB7MYTIvnUcXNmQ=="
        }

        res = requests.get(url, params=params, headers=headers, timeout=10)

        if res.status_code != 200:
            return {"error": "请求微博接口失败"}, 500

        json_data = res.json()

        result = []

        if "page_info" in json_data and "media_info" in json_data["page_info"]:
            result.append(json_data["page_info"]["media_info"])
        elif "mix_media_info" in json_data and "items" in json_data["mix_media_info"]:
            result = []
            for item in json_data["mix_media_info"]["items"]:
                if "data" in item:
                    result.append(item["data"]["media_info"])
        else:
            return {"error": "未找到媒体信息"}, 404

        return result, 200

    except Exception as e:
        return {"error": str(e)}, 500
    
    
