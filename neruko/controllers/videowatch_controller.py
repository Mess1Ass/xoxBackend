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

    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://weibo.com/"  # 必要，防盗链要求
        }
        r = requests.get(video_url, headers=headers, stream=True, timeout=10)
        return Response(
            r.iter_content(chunk_size=4096),
            content_type=r.headers.get("Content-Type", "video/mp4")
        )
    except Exception as e:
        return f"Error: {str(e)}", 500
    
@videowatch_bp.route('/getvedio/b23', methods=['GET'])
def get_b23_video():
    raw_url = request.args.get("url")
    if not raw_url:
        return jsonify({"error": "missing url"}), 400

    data, code = videoWatch_service.get_video_url(raw_url)

    return jsonify({"message": "success", "data": data}), code




