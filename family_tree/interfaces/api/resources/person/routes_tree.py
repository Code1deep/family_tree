 # interfaces/api/resources/person/routes_tree.py
from .routes_crud import person_api  
from flask import jsonify, render_template
from family_tree.interfaces.api.resources.person.init_person_service import person_service
from family_tree.interfaces.api.serializers.person_serializer import PersonSerializer

def register_tree_routes(person_api):
    @person_api.route("/api/visualize/tree/root")
    def get_root_tree():
        try:
            from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
            visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))

            root_person_id = 1 
            tree_data = visualizer.generate_familytree_data(root_person_id)  

            return jsonify(tree_data)
        except Exception as e:
            import traceback
            traceback.print_exc()
            current_app.logger.error(f"Visualization root error: {str(e)}")
            return jsonify({'error': 'Server error'}), 500

     
   @person_api.route('/tree')
   def show_tree():
       from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
       visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
       tree_data = visualizer.generate_familytree_data()
       return render_template('tree.html', nodes=tree_data['nodes'], edges=tree_data['edges'])

   @person_api.route('/api/visualize/tree/<int:person_id>')
   def visualize_tree(person_id):
       try:
           if person_id <= 0:
               abort(400, description="Invalid person ID")
           from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
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

   @person_api.route('/tree/<int:person_id>', methods=['GET'])
       def show_tree_by_id(person_id):
       from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
       visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
       tree_data = visualizer.generate_familytree_data(root_person_id=person_id)

       if current_app.config['TESTING']:
           print(tree_data)
           return jsonify(tree_data)
       else:
           return render_template('tree.html', nodes=tree_data['nodes'], edges=tree_data['edges'])
