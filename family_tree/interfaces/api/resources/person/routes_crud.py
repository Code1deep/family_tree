# interfaces/api/resources/person/routes_crud.py
import logging
from datetime import datetime
from flask import render_template, request, jsonify, abort
from family_tree.interfaces.api.serializers.person_serializer import PersonSerializer
from family_tree.app.extensions import db

def register_crud_routes(person_api, person_service):
    @person_api.route('/persons', methods=['POST'])
    def create_person():
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
                        abort(400, f"Invalid date format for {field}, expected YYYY-MM-DD")
                return None

            birth_date = parse_date('birth_date')
            death_date = parse_date('death_date')

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
    def get_person(person_id):
        person = person_service.get_person_by_id(person_id)
        if not person:
            return jsonify({'error': 'Person not found'}), 404
        return jsonify(person.to_dict()), 200

    @person_api.route('/persons', methods=['GET'])
    def list_persons():
        persons = person_service.get_all_persons()
        return jsonify([PersonSerializer.serialize_for_api(p) for p in persons])

    @person_api.route('/persons/<int:person_id>', methods=['PUT'])
    def update_person_by_service(person_id):
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

    @person_api.route('/persons/<int:person_id>', methods=['DELETE'])
    def delete_person_by_service(person_id):
        try:
            success = person_service.delete_person(person_id)
            if not success:
                return jsonify({'error': 'Person not found'}), 404
            return '', 204
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting person: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @person_api.route('/add')
    def add_person():
        return render_template('add_person.html')

