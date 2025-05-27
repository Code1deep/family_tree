# family_tree/interfaces/api/resources/tree/init_tree_service.py

from flask import Blueprint
from .routes_tree_api import register_tree_api_routes
from .routes_tree_views import register_tree_view_routes

def init_tree_resources(app, person_service):
    """
    Initialise les ressources de l'arbre :
    - Un blueprint pour les routes HTML (interface utilisateur)
    - Un blueprint pour les routes API JSON (backend)
    """

    # 🧩 Blueprint pour les vues HTML (ex : /tree/, /tree/1)
    tree_html_bp = Blueprint("tree_html", __name__)
    register_tree_view_routes(tree_html_bp)
    app.register_blueprint(tree_html_bp, url_prefix="/tree")

    # 🧩 Blueprint pour les routes API JSON (ex : /api/tree/1)
    tree_api_bp = Blueprint("tree_api", __name__)
    register_tree_api_routes(tree_api_bp, person_service)
    app.register_blueprint(tree_api_bp, url_prefix="/api/tree")

