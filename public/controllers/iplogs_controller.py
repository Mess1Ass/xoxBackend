from flask import Blueprint, request, jsonify, Response
import requests
from public.services import iplogs_service

iplogs_bp = Blueprint("iplogs_bp", __name__)

@iplogs_bp.route("/saveip", methods=["GET"])
def collect_ip():
    domain = request.args.get("hostname")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    insert_res, insert_code = iplogs_service.insert_iplog(ip, domain)
    if insert_code != 200:
        return jsonify(insert_res), insert_code
    return jsonify({"message": "success", "data": insert_res}), insert_code
    

@iplogs_bp.route("/getipcnt", methods=["GET"])
def get_visit_count():
    domain = request.args.get("hostname")
    cnt_res, cnt_code = iplogs_service.get_visit_count(domain)
    if cnt_code != 200:
        return jsonify(cnt_res), cnt_code
    return jsonify({"message": "success", "data": cnt_res}), cnt_code