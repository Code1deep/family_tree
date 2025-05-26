# interfaces/api/resources/tree/init_tree_service.py

from family_tree.interfaces.api.resources.tree import tree_api

def init_resources(api):
    """Initialise les ressources de l'arbre généalogique"""
    api.register_blueprint(tree_api)

def create_tree_api():
    """Factory pour créer l'API de l'arbre"""
    return tree_api
