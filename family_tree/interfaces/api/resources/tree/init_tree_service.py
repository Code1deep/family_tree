# interfaces/api/resources/tree/init_tree_service.py

def init_tree_resources(app, person_service):
    """Initialise les ressources de l'arbre avec service injecté"""
    from .routes_tree_api import create_tree_api  # Import local
    tree_api = create_tree_api(person_service)
    app.register_blueprint(tree_api, url_prefix='/tree')

