# family_tree/interfaces/api/resources/tree/init_tree_service.py

from flask import Blueprint, jsonify, render_template
from .routes_tree_api import register_tree_api_routes
from .routes_tree_views import register_tree_view_routes
from family_tree.interfaces.api.resources.person.routes_tree import register_tree_routes, inject_service

def init_tree_resources(app, person_service):
    """
    Initialise les différentes routes liées à l'arbre généalogique :
    - Vue HTML (/tree/)
    - API JSON (/api/tree/)
    - Visualisation D3.js (/api/visualize/tree/)
    """

    # Injecte le service dans les fonctions de visualisation
    inject_service(person_service)

    # ✅ 1. API JSON pour l’arbre généalogique
    api_bp = Blueprint("tree_api_json", __name__)
    register_tree_api_routes(api_bp, person_service)
    app.register_blueprint(api_bp, url_prefix="/api/tree")

    # ✅ 2. Routes HTML (pages)
    html_bp = Blueprint("tree_html_views", __name__)
    register_tree_view_routes(html_bp)
    
    @html_bp.route('/tree_form')
    def show_tree_form():
        return render_template('tree_form.html')
    
    app.register_blueprint(html_bp, url_prefix="/tree")

    # ✅ 3. API pour la visualisation (utilisé par D3.js)
    #viz_bp = Blueprint("tree_visualization_api", __name__)
    #register_tree_routes(viz_bp)
    #app.register_blueprint(viz_bp)
