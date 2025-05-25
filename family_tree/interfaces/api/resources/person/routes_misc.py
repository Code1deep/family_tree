 # interfaces/api/resources/person/routes_misc.py

from flask import jsonify, request

def register_misc_routes(person_api):
    @person_api.route('/api/debug', methods=['POST'])
    def debug_endpoint():
        data = request.get_json()
        return jsonify({"message": "Debug successful", "data": data}), 200

    @person_api.route('/test')
    def test():
        return 'OK'
