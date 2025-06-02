# family_tree/interfaces/api/resources/tree/routes_tree_api.py
from flask import jsonify, current_app
from family_tree.domain.services.tree_service import TreeService
from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
from family_tree.infrastructure.visualization.tree_visualizer import FamilyTreeVisualizer
from family_tree.app.extensions import db

def register_tree_api_routes(bp, person_service):
    """
    Enregistre les routes API JSON pour l’arbre généalogique.
    """

    @bp.route('/<int:person_id>', methods=['GET'])
    def get_tree_json(person_id):
        """
        Endpoint JSON pour générer un arbre généalogique pour une personne donnée.
        """
        if person_id <= 0:
            return jsonify({'error': 'Invalid person ID'}), 400

        try:
            tree_service = TreeService(person_service)
            tree = tree_service.generate_tree(person_id)

            if not tree.get('nodes'):
                return jsonify({'error': 'Person not found'}), 404

            return jsonify(tree), 200

        except Exception as e:
            current_app.logger.error(f"Error generating tree: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @bp.route('/', methods=['GET'])
    def get_default_tree():
        """
        Endpoint JSON pour générer un arbre généalogique global ou par défaut.
        """
        try:
            visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
            tree_data = visualizer.generate_familytree_data()
            return jsonify(tree_data)
        except Exception as e:
            current_app.logger.error(f"Error generating default tree: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
