# family_tree/interfaces/api/resources/tree/init_tree_service.py

from flask import Blueprint
from .routes_tree_api import register_tree_api_routes
from .routes_tree_views import register_tree_view_routes


def create_tree_api(person_service):
    """Crée et configure le blueprint tree_api avec les routes liées à l'arbre"""
    tree_api = Blueprint("tree_api", __name__)

    # Enregistre les routes API JSON
    register_tree_api_routes(tree_api, person_service)

    # Enregistre les routes vues (HTML)
    register_tree_views(tree_api)

    return tree_api


def init_tree_resources(app, person_service):
    """Initialise les ressources de l'arbre avec service injecté"""
    tree_api = create_tree_api(person_service)
    app.register_blueprint(tree_api, url_prefix="/tree")


