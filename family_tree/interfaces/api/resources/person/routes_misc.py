 # interfaces/api/resources/person/routes_misc.py
from flask import jsonify, request

person_service = None

def inject_service(service):
    global person_service
    person_service = service

def register_misc_routes(person_api):
    @person_api.route('/health')
    def health_check():
        return jsonify({'status': 'ok'})
     
    @person_api.route('/api/debug', methods=['POST'])
    def debug_endpoint():
        data = request.get_json()
        return jsonify({"message": "Debug successful", "data": data}), 200

    @person_api.route('/test')
    def test():
        return 'OK'
    
    @person_api.route('stats')
    def get_stats():
        from family_tree.domain.models.person import Person
        males = Person.query.filter_by(gender='M').count()
        females = Person.query.filter_by(gender='F').count()
        living = Person.query.filter(Person.death_date == None).count()
        deceased = Person.query.filter_by(is_alive=False).count()

        return jsonify({
            'males': males,
            'females': females,
            'living': living,
            'deceased': deceased
        })
