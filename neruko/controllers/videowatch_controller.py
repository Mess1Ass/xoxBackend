from flask import Blueprint, request, jsonify, Response
import requests
from neruko.services import videoWatch_service

videowatch_bp = Blueprint("videowatch_bp", __name__)

@videowatch_bp.route('/getvedio/weibo', methods=['GET'])
def get_weibo_video():
    weibo_id = request.args.get("weibo_id")
    res, code = videoWatch_service.get_weibo_vedio_detail(weibo_id)
    if(code != 200):
        return res, code
    return jsonify({"message": "success", "data": res}), code

@videowatch_bp.route('/proxy')
def proxy_video():
    video_url = request.args.get("url")
    if not video_url:
        return "Missing url", 400

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
        ),
        "Referer": "https://weibo.com/"
    }
    try:
        r = requests.get(video_url, headers=headers, stream=True, timeout=10)

        if r.status_code != 200:
            return Response("视频获取失败", status=500)

        return Response(
            r.iter_content(chunk_size=4096),
            mimetype="video/mp4",
            direct_passthrough=True
        )
    except Exception as e:
        return Response(f"请求视频时出错: {e}", status=500)
    
@videowatch_bp.route('/getvedio/b23', methods=['GET'])
def get_b23_video():
    raw_url = request.args.get("url")
    if not raw_url:
        return jsonify({"error": "missing url"}), 400

    data, code = videoWatch_service.get_video_url(raw_url)

    return jsonify({"message": "success", "data": data}), code




