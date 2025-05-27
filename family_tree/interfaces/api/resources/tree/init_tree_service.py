# family_tree/interfaces/api/resources/tree/init_tree_service.py

from flask import Blueprint
from .routes_tree_api import register_tree_api_routes
from .routes_tree_views import register_tree_view_routes
from family_tree.interfaces.api.resources.person.routes_tree import register_tree_routes, inject_service

def init_tree_resources(app, person_service):
    """
    Initialise les différentes routes liées à l'arbre généalogique :
    - Vue HTML (ex: /tree/, /tree/1)
    - API JSON (ex: /api/tree/1)
    - API de visualisation (ex: /api/visualize/tree/1)
    """

    # ✅ Injection du service dans routes_tree
    inject_service(person_service)
    
    # ✅ Blueprint pour les routes de visualisation (ex: /tree/<id>, /api/visualize/tree/<id>)
    visualize_bp = Blueprint('tree_visualization', __name__)
    register_tree_routes(visualize_bp)
    app.register_blueprint(visualize_bp)

    # ✅ Blueprint pour les vues HTML classiques (ex: /tree/, /tree/1)
    tree_html_bp = Blueprint("tree_html", __name__)
    register_tree_view_routes(tree_html_bp)
    app.register_blueprint(tree_html_bp, url_prefix="/tree")

    # ✅ Blueprint pour les API spécifiques à l'arbre (si différentes, sinon inutile)
    tree_api_bp = Blueprint("tree_api_json", __name__)
    register_tree_api_routes(tree_api_bp, person_service)
    app.register_blueprint(tree_api_bp, url_prefix="/api/tree")

