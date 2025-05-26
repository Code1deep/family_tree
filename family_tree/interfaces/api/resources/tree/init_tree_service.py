# interfaces/api/resources/tree/init_tree_service.py

# from family_tree.interfaces.api.resources.tree import tree_api
def init_tree_resources(app):
    """Initialise les ressources de l'arbre"""
    from . import tree_api  # Import local pour éviter les circulaires
    app.register_blueprint(tree_api, url_prefix='/tree')
