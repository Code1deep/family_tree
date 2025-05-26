# interfaces/api/resources/tree/routes_crud.py

from flask import request, jsonify
from family_tree.services.tree_service import TreeService

def register_crud_routes(blueprint):
    """Enregistre les routes CRUD de l'arbre"""
    
    @blueprint.route('/tree', methods=['GET'])
    def show_tree():
        return TreeService.render_tree_template()
    
    @blueprint.route('/tree/add', methods=['GET', 'POST'])
    def add_to_tree():
        if request.method == 'POST':
            return TreeService.handle_add_to_tree(request.form)
        return TreeService.render_add_form()
