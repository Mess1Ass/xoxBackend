from flask import Blueprint, request, jsonify, Response
import requests
from neruko.services import showtimetable_service

showlogs_bp = Blueprint("showlogs_bp", __name__)

@showlogs_bp.route("/insertShowLog", methods=["POST"])
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

@showlogs_bp.route("/getShowLogs", methods=["GET"])
def get_all_showlog():

    res, code = showtimetable_service.find_all_showlog()
    if res != 200:
        return jsonify(res), code
    return jsonify({"message": "success", "data": res}), code