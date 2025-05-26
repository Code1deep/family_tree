# interfaces/api/resources/tree/routes_api.py

from flask import jsonify
from family_tree.services.tree_service import TreeService

def register_api_routes(blueprint):
    """Enregistre les routes API de l'arbre"""
    
    @blueprint.route('/api/tree', methods=['GET'])
    def get_tree():
        tree_data = TreeService.get_full_tree()
        return jsonify(tree_data)
    
    @blueprint.route('/api/tree/<int:person_id>', methods=['GET'])
    def get_person_tree(person_id):
        person_tree = TreeService.get_person_subtree(person_id)
        return jsonify(person_tree)
