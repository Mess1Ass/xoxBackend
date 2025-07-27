from flask import Blueprint, request, jsonify
from neruko.services import focuslink_service


focuslink_bp = Blueprint("focuslink_bp", __name__)

@focuslink_bp.route("/insertfolink", methods=["POST"])
def insert_focuslink():
    data = request.json
    date = data.get("date")
    title = data.get("title")
    links = data.get("links")
    
    if not date or not title or not links:
        return {"error": "未填写完全"}, 400
    
    res, code = focuslink_service.insert_focuslink(date, title, links)
    if(code != 200):
        return res, code
    return jsonify({"message": "success", "id": str(res)}), code

@focuslink_bp.route("/getAll", methods=["GET"])
def find_all_focusLink():
    res, code = focuslink_service.find_all_data()
    if(code != 200):
        return res, code
    return jsonify({"message": "success", "data": res}), code
