# family_tree/app/__init__.py
from flask import app, current_app, request
from .factory import create_app
import logging.config
from family_tree.config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)

@app.before_request
def log_request_info():
    current_app.logger.info(f"[ROUTE] {request.method} {request.path}")
    if request.json:
        current_app.logger.info(f"[BODY] {request.json}")
    if request.args:
        current_app.logger.info(f"[ARGS] {request.args}")
    if request.form:
        current_app.logger.info(f"[FORM] {request.form}")

@app.after_request
def log_response_info(response):
    current_app.logger.info(f"[RESPONSE] {response.status} {response.content_type}")
    return response
