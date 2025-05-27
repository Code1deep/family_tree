# family_tree/interfaces/api/resources/tree/routes_tree_api.py

from flask import Blueprint, jsonify, current_app
from family_tree.domain.services.tree_service import TreeService

def register_tree_api_routes(tree_api_bp, person_service):
    """
    Enregistre la route API JSON de génération d'arbre généalogique.
    """

    @tree_api_bp.route('/<int:person_id>')
    def get_tree_json(person_id):
        """
        Endpoint JSON unifié pour générer un arbre généalogique :
        - IDs invalides
        - Personnes non trouvées
        - Partenaires, familles, photos
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

    return tree_api_bp

