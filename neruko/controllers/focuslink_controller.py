from flask import Blueprint, request, jsonify
from neruko.services import focuslink_service


focuslink_bp = Blueprint("focuslink_bp", __name__)

@focuslink_bp.route("/insertfolink", methods=["POST"])
def insert_focuslink():
    data = request.json or {}
    date = data.get("date")
    title = data.get("title")
    links = data.get("links")
    
    if not date or not title or not links:
        return jsonify({"error": "未填写完全"}), 400
    
    res, code = focuslink_service.insert_focuslink(date, title, links)
    if(code != 200):
        return jsonify(res), code
    return jsonify({"message": "success", "id": str(res)}), code

@focuslink_bp.route("/getAll", methods=["GET"])
def find_all_focusLink():
    res, code = focuslink_service.find_all_data()
    if(code != 200):
        return jsonify(res), code
    return jsonify({"message": "success", "data": res}), code

@focuslink_bp.route("/updatefolink", methods=["POST"])
def update_folink():
    data = request.json or {}
    _id = data.get("_id")
    date = data.get("date")
    title = data.get("title")
    links = data.get("links")
    
    if not date or not title or not links:
        return jsonify({"error": "未填写完全"}), 400
    
    res, code = focuslink_service.update_focuslink(_id, date, title, links)
    if(code != 200):
        return jsonify(res), code
    return jsonify({"message": "success"}), code

@focuslink_bp.route("/deletefolink", methods=["POST"])
def delete_folink():
    _id = request.args.get("id")  # 从 URL 参数中取出 id

    if not _id:
        return jsonify({"error": "缺少参数 id"}), 400
    
    res, code = focuslink_service.delete_focuslink(_id)
    if(code != 200):
        return jsonify(res), code
    return jsonify({"message": "success"}), code
