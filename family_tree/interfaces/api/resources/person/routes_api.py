@ routes_api.py
from .routes_crud import person_api  # Import du blueprint existant

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
