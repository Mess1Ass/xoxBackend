import requests
import json
import re
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
            result.append({"title": json_data["text"], "video_url": json_data["page_info"]["media_info"]["stream_url"]})
        elif "mix_media_info" in json_data and "items" in json_data["mix_media_info"]:
            result = []
            for item in json_data["mix_media_info"]["items"]:
                if "data" in item:
                    result.append({"title": json_data["text"], "video_url": item["data"]["media_info"]["stream_url"]})
        else:
            return {"error": "未找到媒体信息"}, 404

        return result, 200

    except Exception as e:
        return {"error": str(e)}, 500

def expand_short_url(url):
    # 模拟浏览器请求头
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com",
    }
    """短链解码为长链"""
    res = requests.get(url, headers=HEADERS, allow_redirects=True)
    return res.url if res.status_code == 200 else None

def extract_bvid(url):
    """从链接中提取BV号"""
    match = re.search(r"(BV\w+)", url)
    return match.group(1) if match else None

def extract_page_number(url):
    """
    如果 URL 中包含参数 p=数字，返回该数字（int）。
    如果不包含，返回 -1。
    """
    match = re.search(r"[?&]p=(\d+)", url)
    return int(match.group(1)) if match else -1

def get_video_url(url):
    result = []

    if "b23.tv" in url:
        real_url = expand_short_url(url)
        if not real_url:
            return {"error": "短链解析失败"}, 400
    else:
        real_url = url

    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com",
    }

    bvid = extract_bvid(real_url)
    if not bvid:
        return {"error": "未能提取 BV 号"}, 400

    page = extract_page_number(real_url)

    # 获取视频信息
    api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    res = requests.get(api_url, headers=HEADERS).json()

    if res.get("code") != 0:
        return {"error": "视频信息获取失败"}, 500

    data = res["data"]
    title = data.get("title", "")

    # 分P情况
    if page != -1:
        try:
            cid = data["pages"][page - 1]["cid"]
        except IndexError:
            return {"error": "页码超出范围"}, 400
        play_url = f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=80&fnval=1"
        play_res = requests.get(play_url, headers=HEADERS).json()
        video_url = play_res["data"]["durl"][0]["url"]
        result.append({"title": f"{title} - P{page}", "video_url": video_url})
        return result, 200

    # 合集（分集剧集）处理
    if data.get("is_season_display"):
        for ep in data["ugc_season"]["sections"][0]["episodes"]:
            cid = ep["cid"]
            ep_bvid = ep["bvid"]
            ep_title = ep["title"]
            play_url = f"https://api.bilibili.com/x/player/playurl?bvid={ep_bvid}&cid={cid}&qn=80&fnval=1"
            play_res = requests.get(play_url, headers=HEADERS).json()
            video_url = play_res["data"]["durl"][0]["url"]
            result.append({"title": ep_title, "video_url": video_url})
        return result, 200

    # 单视频（默认P1）
    cid = data["pages"][0]["cid"]
    play_url = f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=80&fnval=1"
    play_res = requests.get(play_url, headers=HEADERS).json()
    video_url = play_res["data"]["durl"][0]["url"]
    result.append({"title": title, "video_url": video_url})
    return result, 200




