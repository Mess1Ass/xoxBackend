from flask import Blueprint, request, jsonify, Response
import requests
from natsumi.services import showtimetable_service

showlogs_bp_natsumi = Blueprint("showlogs_bp_natsumi", __name__)

@showlogs_bp_natsumi.route("/natsumi/insertShowLog", methods=["POST"])
def insert_showlog():
    data = request.json or {}
    endTime = data.get("endTime")
    startTime = data.get("startTime")
    title = data.get("title")
    location = data.get("location")

    res, code = showtimetable_service.insert_showlog(title, startTime, endTime, location)
    if res != 200:
        return jsonify(res), code
    return jsonify({"message": "success", "data": res}), code

@showlogs_bp_natsumi.route("/natsumi/getShowLogs", methods=["GET"])
def get_all_showlog():

    res, code = showtimetable_service.find_all_showlog()
    if res != 200:
        return jsonify(res), code
    return jsonify({"message": "success", "data": res}), code

@showlogs_bp_natsumi.route("/natsumi/getEarliestShowLog", methods=["GET"])
def get_earliest_showlog():
    res, code = showtimetable_service.find_earliest_showlog()
    if res != 200:
        return jsonify(res), code
    return jsonify({"message": "success", "data": res}), code

@showlogs_bp_natsumi.route("/natsumi/updateShowLog", methods=["POST"])
def update_showlog():
    data = request.json or {}
    _id = data.get("_id")
    startTime = data.get("startTime")
    title = data.get("title")
    endTime = data.get("endTime")
    location = data.get("location")

    
    if not location or not endTime or not title or not startTime:
        return jsonify({"error": "未填写完全"}), 400
    
    res, code = showtimetable_service.update_showlog(_id, title, startTime, endTime, location)
    if(code != 200):
        return jsonify(res), code
    return jsonify({"message": "success"}), code

@showlogs_bp_natsumi.route("/natsumi/deleteShowLog", methods=["POST"])
def delete_showlog():
    _id = request.args.get("id")  # 从 URL 参数中取出 id

    if not _id:
        return jsonify({"error": "缺少参数 id"}), 400
    
    res, code = showtimetable_service.delete_showlog(_id)
    if(code != 200):
        return jsonify(res), code
    return jsonify({"message": "success"}), code