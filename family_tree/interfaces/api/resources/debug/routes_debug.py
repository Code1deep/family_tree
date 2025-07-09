# Ajoute dans un routes_debug.py par ex
from flask import Blueprint, jsonify
import sys

debug_bp = Blueprint('debug', __name__)

@debug_bp.route("/debug/modules")
def show_modules():
    return jsonify(list(sys.modules.keys()))
