# family_tree/interfaces/api/resources/debug/routes_debug.py
from flask import Blueprint, jsonify
import sys

debug_bp = Blueprint('debug', __name__)

@debug_bp.route("/debug/modules")
def show_modules():
    return jsonify(list(sys.modules.keys()))
