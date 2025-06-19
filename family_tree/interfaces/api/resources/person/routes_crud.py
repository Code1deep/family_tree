# interfaces/api/resources/person/routes_crud.py
import logging
from datetime import datetime
from flask import render_template, request, jsonify, abort
from family_tree.domain.services.person_service import PersonService
from family_tree.app.extensions import db
from family_tree.interfaces.api.serializers.person_serializer import PersonSerializer
from typing import Optional, cast

person_service: Optional[PersonService] = None

def check_service() -> PersonService:
    """Vérifie que le service est bien initialisé et retourne un PersonService"""
    global person_service
    if person_service is None:
        raise RuntimeError("❌ person_service is not initialized. Please inject_service() before using routes.")
    return cast(PersonService, person_service)

def inject_service(service: PersonService):
    global person_service
    person_service = service
    print(f"✅ inject_service() appelé avec {service}")

def register_crud_routes(person_api):
    @person_api.route('/crud/person/<int:person_id>', methods=['DELETE'])
    def delete_person(person_id):
        service = check_service()
        success = service.delete_person(person_id)
        if success:
            return jsonify({'success': True}), 204
        abort(404, "Person not found")

    @person_api.route('/persons', methods=['POST'])
    def create_person():
        service = check_service()
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        try:
            required_fields = ['first_name', 'last_name', 'gender']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f"Missing required field: {field}"}), 400

            def parse_date(field):
                value = data.get(field)
                if value:
                    try:
                        return datetime.strptime(value, "%Y-%m-%d").date()
                    except ValueError:
                        return jsonify({'error': f"Invalid date format for {field}, expected YYYY-MM-DD"}), 400
                return None

            birth_date = parse_date('birth_date')
            if isinstance(birth_date, tuple): return birth_date
            death_date = parse_date('death_date')
            if isinstance(death_date, tuple): return death_date

            person = service.create_person(
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
    def get_person(person_id):
        service = check_service()
        person = service.get_person_by_id(person_id)
        if not person:
            return jsonify({'error': 'Person not found'}), 404
        return jsonify(person.to_dict()), 200

    @person_api.route('/persons', methods=['GET'])
    def list_persons():
        service = check_service()
        persons = service.get_all_persons()
        return jsonify([PersonSerializer.serialize_for_api(p) for p in persons])

    @person_api.route('/persons/<int:person_id>', methods=['PUT'])
    def update_person_by_service(person_id):
        service = check_service()
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        try:
            updated_person = service.update_person(person_id, data)
            if not updated_person:
                return jsonify({'error': 'Person not found'}), 404
            return jsonify(updated_person), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating person: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @person_api.route('/persons/<int:person_id>', methods=['DELETE'])
    def delete_person_by_service(person_id):
        service = check_service()
        try:
            success = service.delete_person(person_id)
            if not success:
                return jsonify({'error': 'Person not found'}), 404
            return '', 204
        except Exception as e:
            logging.error(f"Error deleting person: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @person_api.route('/add')
    def add_person():
        return render_template('add_person.html')


