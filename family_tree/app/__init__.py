# family_tree/app/__init__.py
from flask import Flask, app, current_app, request
from family_tree.app.factory import create_app
import logging.config
from family_tree.app.config import LOGGING_CONFIG
logging.config.dictConfig(LOGGING_CONFIG)

@app.after_request
def log_response_info(response):
    current_app.logger.info(f"[RESPONSE] {response.status} {response.content_type}")
    return response
