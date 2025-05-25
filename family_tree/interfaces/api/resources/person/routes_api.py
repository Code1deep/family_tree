# interfaces/api/resources/person/routes_api.py
from .routes_crud import person_api  
from flask import request, jsonify
from family_tree.interfaces.api.resources.person.init_person_service import person_service
from family_tree.interfaces.api.serializers.person_serializer import PersonSerializer

def register_api_routes(bp):
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
