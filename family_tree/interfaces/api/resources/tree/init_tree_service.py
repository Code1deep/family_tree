# family_tree/interfaces/api/resources/tree/init_tree_service.py
from flask import Blueprint, jsonify, render_template
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
    
    # 1️⃣ Blueprint principal 'tree_api' (existant)
    tree_api = Blueprint('tree_api', __name__)
    register_tree_routes(tree_api)  # Routes existantes
    
    # Ajout de la nouvelle route /api/stats
    @tree_api.route('/stats')
    def get_stats():
        return jsonify({
            'total': person_service.count_persons(),
            'depth': person_service.get_tree_depth(),
            'living': person_service.count_living(),
            'genders': person_service.count_by_gender()
        })
    
    app.register_blueprint(tree_api, url_prefix='/api/tree')

    # 2️⃣ Blueprint 'tree_views' pour HTML (existant)
    tree_views = Blueprint('tree_views', __name__)
    register_tree_view_routes(tree_views)
    
    # Ajout de la nouvelle route /tree_form
    @tree_views.route('/form')
    def show_tree_form():
        return render_template('tree_form.html')
    
    app.register_blueprint(tree_views, url_prefix='/tree')

    # 3️⃣ Blueprint complémentaire (optionnel)
    tree_viz = Blueprint('tree_visualization', __name__)
    tree_viz.add_url_rule('/visualize/<int:person_id>', 'visualize', 
                         lambda person_id: jsonify(person_service.get_tree_data(person_id)))
    app.register_blueprint(tree_viz, url_prefix='/api')

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

