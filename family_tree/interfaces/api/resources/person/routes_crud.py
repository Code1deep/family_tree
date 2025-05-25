from flask import Blueprint, jsonify, request

person_api = Blueprint('person_api', __name__)  # Nom original conservé

@person_api.route('/persons', methods=['POST'])
def create_person():  # Nom original
    """Endpoint POST /persons - Création personne"""
    """Créer une personne via /persons"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        # Vérification explicite des champs obligatoires
        required_fields = ['first_name', 'last_name', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f"Missing required field: {field}"}), 400

        # 🔁 Conversion des dates
        def parse_date(field):
            value = data.get(field)
            if value:
                try:
                    return datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    return jsonify({'error': f"Invalid date format for {field}, expected YYYY-MM-DD"}), 400
            return None

        birth_date = parse_date('birth_date')
        if isinstance(birth_date, tuple): return birth_date  # early return if error
        death_date = parse_date('death_date')
        if isinstance(death_date, tuple): return death_date

        person = person_service.create_person(
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender=data['gender'],
            birth_date=birth_date,
            death_date=death_date,
            mother_id=data.get('mother_id'),
            father_id=data.get('father_id')
        )
        return jsonify(person.to_dict()), 201

    except Exception as e:
        logging.error(f"Error creating person: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@person_api.route('/persons/<int:person_id>', methods=['GET'])
def get_per_son_s(person_id):
    """Récupérer une personne par ID via /persons"""
    person = person_service.get_person_by_id(person_id)
    if not person:
        return jsonify({'error': 'Person not found'}), 404
    return jsonify(person.to_dict()), 200
