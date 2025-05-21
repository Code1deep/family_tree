# interfaces\api\resources\tree_resource.py
from setup_path import setup_sys_path
setup_sys_path(__file__)

from flask import Blueprint, current_app, jsonify, request
from domain.services.tree_service import TreeService

def create_tree_api(person_service):
    """
    Crée et configure le Blueprint Flask pour les API d'arbre généalogique.
    """
    tree_api_bp = Blueprint('tree_api', __name__)
    #tree_api = Api(tree_api_bp)

    @tree_api_bp.route('/tree/<person_id>')
    def get_tree(person_id):
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

    @tree_api_bp.route('/persons', methods=['POST'])
    def create_person():
        """
        Création d'une personne via JSON
        """
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid input'}), 400

        try:
            person = person_service.create_person(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                gender=data.get('gender'),
                birth_date=data.get('birth_date'),
                death_date=data.get('death_date'),
                mother_id=data.get('mother_id'),
                father_id=data.get('father_id')
            )

            return jsonify(person.to_dict()), 201
        except Exception as e:
            current_app.logger.error(f"Error creating person: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

    return tree_api_bp
