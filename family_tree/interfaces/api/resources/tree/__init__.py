# interfaces/api/resources/tree/__init__.py
from flask import Blueprint
from .routes_tree_api import create_tree_api
from .routes_tree_views import register_tree_views

tree_api = Blueprint('tree_api', __name__)

# Initialise les routes
tree_api = create_tree_api()
register_tree_views(tree_api)
