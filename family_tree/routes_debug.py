# family_tree/routes_debug.py

from flask import Blueprint, jsonify
from app.extensions import db
from sqlalchemy import inspect

debug_bp = Blueprint("debug_bp", __name__)

@debug_bp.route("/api/debug/persons-columns")
def persons_columns():
    insp = inspect(db.engine)
    if "persons" in insp.get_table_names():
        cols = insp.get_columns("persons")
        return jsonify([col["name"] for col in cols])
    return jsonify({"error": "Table 'persons' inexistante"})
