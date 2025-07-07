# interfaces/api/routes_admin.py
from flask import Blueprint, request, jsonify
import os

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/admin/init")
def trigger_full_initialize():
    token = request.args.get("token")
    if token != os.getenv("INIT_TOKEN", "secret"):
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify({"status": "Initialization triggered"}), 200
