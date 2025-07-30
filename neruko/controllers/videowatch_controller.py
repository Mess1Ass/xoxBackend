from flask import Blueprint, request, jsonify
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

@videowatch_bp.route('/getvedio/b23', methods=['GET'])
def get_bilibili_video():
    b23_id = request.args.get("b23_id")
    res, code = videoWatch_service.get_b23_vedio_detail(b23_id)
    if(code != 200):
        return res, code
    return jsonify({"message": "success", "data": res}), code




