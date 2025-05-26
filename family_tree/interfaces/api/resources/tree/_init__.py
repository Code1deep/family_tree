# interfaces/api/resources/tree/_init__.py

from flask import Blueprint
from family_tree.interfaces.api.resources.tree.routes_api import register_api_routes
from family_tree.interfaces.api.resources.tree.routes_crud import register_crud_routes
from family_tree.interfaces.api.resources.tree.init_tree_service import init_resources, create_tree_api

tree_api = Blueprint('tree_api', __name__)

register_api_routes(tree_api)
register_crud_routes(tree_api)
