# \interfaces\api\resources\person_resource.py
# -*- coding: utf-8 -*-
import traceback
import logging
from datetime import datetime

from flask import Blueprint, current_app, render_template, request, jsonify, abort

from setup_path import setup_sys_path
setup_sys_path(__file__)

from app.extensions import db
from domain.models.person import Person
from domain.services.person_service import PersonService
from interfaces.api.serializers.person_serializer import PersonSerializer
from infrastructure.visualization.tree_visualizer import FamilyTreeVisualizer
from infrastructure.persistence.repositories.person_repo import PersonRepository
from infrastructure.visualization.tree_visualizer import get_visualizer

person_api = Blueprint('person_api', __name__)
person_service = None

def init_resources(db_session):
    global person_service
    from infrastructure.persistence.repositories.person_repo import PersonRepository
    repo = PersonRepository(db_session)
    person_service = PersonService(repo)

# ----------- ROUTES POUR /persons gender -------------

from datetime import datetime

@person_api.route('/persons', methods=['POST'])
def create_person():
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

@person_api.route('/persons', methods=['GET'])
def list_persons():
    """✅ Retourne toutes les personnes avec leurs champs API complets"""
    persons = person_service.get_all_persons()
    return jsonify([PersonSerializer.serialize_for_api(p) for p in persons])

# ✅ Doublon supprimé :
# def get_all_persons(person_id): ...
# ❌ Supprimé car c’est un doublon exact du `@person_api.route('/persons', methods=['GET'])` ci-dessus.
# ⚠️ De plus, l’argument `person_id` n’a pas de sens ici pour une route qui retourne toutes les personnes.

@person_api.route('/persons/<int:person_id>', methods=['PUT'])
def update_person_by_service(person_id):
    """✅ Définition conservée — met à jour une personne via service"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        person = person_service.get_person_by_id(person_id)
        if not person:
            return jsonify({'error': 'Person not found'}), 404

        for field in ['first_name', 'last_name', 'gender', 'birth_date', 'death_date', 'mother_id', 'father_id']:
            if field in data:
                setattr(person, field, data[field])

        db.session.commit()
        return jsonify(person.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating person: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# ✅ Doublon supprimé :
# def update_person(person_id): (celui avec Person.query.get)
# ❌ Supprimé car même méthode + chemin
# ❗ L'autre version utilise le service, ce qui respecte mieux la couche métier. On garde celle-là.

@person_api.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person_by_service(person_id):
    try:
        success = person_service.delete_person(person_id)
        if not success:
            return jsonify({'error': 'Person not found'}), 404
        return '', 204
    except Exception as e:
        person_service.repo.rollback()  # Assure-toi que rollback() existe
        logging.error(f"Error deleting person: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# ✅ Doublon supprimé :
# def delete_person(person_id): (celui avec Person.query.get)
# ❌ Supprimé car redondant avec celui du service (meilleure approche DDD)

# ---------- ROUTES POUR /person (au singulier) -----------

@person_api.route('/person', methods=['GET', 'POST'])
def create_person_api():
    """Crée une personne via /person"""
    data = request.get_json()
    for date_field in ['birth_date', 'death_date']:
        if data.get(date_field):
            try:
                data[date_field] = datetime.strptime(data[date_field], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': f'Invalid format for {date_field}, expected YYYY-MM-DD'}), 400
            
    required_fields = ['first_name', 'last_name', 'gender']
    if not all(field in data for field in required_fields):
        abort(400, f"Missing required fields: {required_fields}")

    try:
        new_person = person_service.create_person(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            birth_date=data.get('birth_date'),
            gender=data.get('gender'),
            death_date=data.get('death_date'),
            mother_id=data.get('mother_id'),
            father_id=data.get('father_id')
        )
        db.session.commit()
        return jsonify(PersonSerializer.serialize_for_api(new_person)), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create person error: {str(e)}")
        abort(500, "Internal server error")

@person_api.route('/api/person/<int:person_id>')
def get_person_by_id(person_id):
    person = person_service.get_by_id(person_id)
    if not person:
        abort(404, "Person not found")
    return jsonify(person)

@person_api.route('/api/person/<int:person_id>/children')
def get_person_children(person_id):
    children = person_service.get_children(person_id)
    return jsonify([PersonSerializer.serialize_basic(c) for c in children])

@person_api.route('/api/person')
def get_person():
    person_id = request.args.get('id', type=int)
    if not person_id:
        abort(400, "Missing person id")
    
    include = request.args.get('include', '')
    try:
        if 'relatives' in include:
            return jsonify(person_service.get_with_relatives(person_id))
        return jsonify(person_service.get_basic(person_id))
    except ValueError as e:
        abort(404, str(e))

@person_api.route('/api/persons', methods=['GET'])
def search_persons():
    name = request.args.get('name')
    gender = request.args.get('gender')

    query = Person.query

    if name and name.strip() != '':
        query = query.filter(
            (Person.first_name.ilike(f"%{name}%")) |
            (Person.last_name.ilike(f"%{name}%"))
        )

    if gender:
        query = query.filter(Person.gender.ilike(gender))  # 'F', 'M', etc.

    persons = query.all()
    return jsonify([p.to_dict() for p in persons]), 200


# ----------------- DEBUG ET TEST -------------------

@person_api.route('/api/debug', methods=['POST'])
def debug_endpoint():
    data = request.get_json()
    return jsonify({"message": "Debug successful", "data": data}), 200

@person_api.route('/test')
def test():
    return "L'application fonctionne 🎉"

# ----------------- VISUALISATION ARBRE -------------------

@person_api.route("/api/visualize/tree/root")
def get_root_tree():
    try:
        from infrastructure.persistence.repositories.person_repo import PersonRepository
        visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
        tree_data = visualizer.generate_familytree_data()  # Pas besoin de None ici
        return jsonify(tree_data)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.error(f"Visualization root error: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

@person_api.route('/api/visualize/tree/<int:person_id>')
def visualize_tree(person_id):
    try:
        if person_id <= 0:
            abort(400, description="Invalid person ID")
        from infrastructure.persistence.repositories.person_repo import PersonRepository
        visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
        tree_data = visualizer.generate_familytree_data(person_id)
        if not tree_data["nodes"] and not tree_data["edges"]:
            return jsonify({'error': 'Person not found'}), 404
        print(tree_data)
        return jsonify(tree_data)
    except Exception as e:
        traceback.print_exc()
        current_app.logger.error(f"Visualization error: {str(e)}")
        return jsonify({'error': 'Server error'}), 500

@person_api.route('/tree')
def show_tree():
    from infrastructure.persistence.repositories.person_repo import PersonRepository
    visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
    tree_data = visualizer.generate_familytree_data()
    return render_template('tree.html', nodes=tree_data['nodes'], edges=tree_data['edges'])

@person_api.route('/tree/<int:person_id>', methods=['GET'])
def show_tree_by_id(person_id):
    from infrastructure.persistence.repositories.person_repo import PersonRepository
    visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
    tree_data = visualizer.generate_familytree_data(root_person_id=person_id)

    if current_app.config['TESTING']:
        print(tree_data)
        return jsonify(tree_data)
    else:
        return render_template('tree.html', nodes=tree_data['nodes'], edges=tree_data['edges'])


# ------------ INIT POUR INJECTION DE SERVICE (tests) -----------

def create_person_api(service):
    global person_service
    person_service = service
    return person_api
