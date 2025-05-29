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
    
    @person_api.route('/api/stats')
    def get_stats():
        stats = {
            'males': 10,
            'females': 12,
            'living': 15,
            'deceased': 7
        }
        return jsonify(stats)
