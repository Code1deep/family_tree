# family_tree/interfaces/api/resources/tree/init_tree_service.py

from flask import Blueprint, jsonify, render_template

from .routes_tree_api import register_tree_api_routes
from .routes_tree_views import register_tree_view_routes
from family_tree.interfaces.api.resources.person.routes_tree import inject_service


def init_tree_resources(app, person_service):
    """
    Initialise les différentes routes liées à l'arbre généalogique :
    - Vue HTML (ex: /tree/, /tree/1)
    - API JSON (ex: /api/tree/1)
    - API de visualisation (ex: /api/visualize/tree/1)
    """

    # ✅ Injection du service dans les routes
    inject_service(person_service)

    # ────────────────────────────────────────────────
    # 1️⃣ Routes API JSON de l’arbre (ex: /api/tree/1)
    # ────────────────────────────────────────────────
    tree_api_bp = Blueprint("tree_api_json", __name__)
    register_tree_api_routes(tree_api_bp, person_service)

    # ➕ Route complémentaire : statistiques JSON
    @tree_api_bp.route('/stats')
    def get_stats():
        return jsonify({
            'total': person_service.count_persons(),
            'depth': person_service.get_tree_depth(),
            'living': person_service.count_living(),
            'genders': person_service.count_by_gender()
        })

    app.register_blueprint(tree_api_bp, url_prefix="/api/tree")

    # ──────────────────────────────────────────────────────
    # 2️⃣ Routes API de visualisation (ex: /api/visualize/42)
    # ──────────────────────────────────────────────────────
    tree_viz_bp = Blueprint('tree_visualization_api', __name__)
    tree_viz_bp.add_url_rule(
        '/visualize/<int:person_id>',
        'visualize',
        lambda person_id: jsonify(person_service.get_tree_data(person_id))
    )

    app.register_blueprint(tree_viz_bp, url_prefix='/api')

    # ────────────────────────────────────────────────
    # 3️⃣ Routes HTML (ex: /tree/, /tree/1, /tree_form)
    # ────────────────────────────────────────────────
    tree_html_bp = Blueprint("tree_html", __name__)
    register_tree_view_routes(tree_html_bp)

    # ➕ Vue complémentaire : formulaire
    @tree_html_bp.route('/tree_form')
    def show_tree_form():
        return render_template('tree_form.html')

    app.register_blueprint(tree_html_bp, url_prefix="/tree")
