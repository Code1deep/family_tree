#  interfaces/api/resources/tree/routes_tree_api.py

from flask import Blueprint, jsonify, request, current_app, render_template
from family_tree.interfaces.api.serializers.person_serializer import PersonSerializer

from family_tree.domain.services.tree_service import TreeService

def register_tree_api_routes(tree_api_bp, person_service):
    """
    Enregistre les routes API JSON liées à l'arbre généalogique.
    """
    @tree_api_bp.route('/<int:person_id>')
   def get_tree(person_id):
        """
        Endpoint unifié pour générer un arbre généalogique.
        Gère les cas d'erreurs : ID invalide, personne non trouvée, etc.
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

    @tree_api_bp.route('/<person_id>')
    def get_tree_json(person_id):
            """
            Endpoint unifié gérant tous les cas de test :
            - IDs invalides
            - Personnes non trouvées
            - Partenaires
            - Grandes familles
            - Photos
            """
            try:
                person_id = int(person_id)
            except ValueError:
                return jsonify({'error': 'Invalid person ID'}), 400

            if person_id <= 0:
                return jsonify({'error': 'Invalid person ID'}), 400

            try:
                tree_service = TreeService(person_service)
                tree = tree_service.generate_tree(person_id)

                if not tree.get('nodes'):
                    return jsonify({'error': 'Person not found'}), 404
                print(tree)
                return jsonify(tree), 200

            except Exception as e:
                current_app.logger.error(f"Error generating tree: {str(e)}")
                return jsonify({'error': 'Internal server error'}), 500

    return tree_api_bp

