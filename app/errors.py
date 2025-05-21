# app/errors.py
from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    return jsonify(message="Resource not found"), 404

@errors.app_errorhandler(405)
def method_not_allowed_error(error):
    return jsonify(message="Method not allowed"), 405

@errors.app_errorhandler(500)
def internal_server_error(error):
    return jsonify(message="Internal server error"), 500

@errors.app_errorhandler(400)
def bad_request(error):
    return jsonify({"message": "Bad request"}), 400
