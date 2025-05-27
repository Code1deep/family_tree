# interfaces/api/resources/tree/init_tree_service.py

from flask import Blueprint

def create_tree_api(app, person_service):
    tree_api = Blueprint("tree_api", __name__)

    @tree_api.route("/tree")
    def tree_view():
        return "Tree API working"

    app.register_blueprint(tree_api)

def init_tree_resources(app, person_service):
    """Initialise les ressources de l'arbre avec service injecté"""
    from .routes_tree_api import create_tree_api  # Import local
    tree_api = create_tree_api(person_service)
    app.register_blueprint(tree_api, url_prefix='/tree')

