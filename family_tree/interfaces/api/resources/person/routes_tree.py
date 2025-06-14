# interfaces/api/resources/person/routes_tree.py
from flask import jsonify, render_template, abort, current_app
from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
from family_tree.infrastructure.visualization.tree_visualizer import FamilyTreeVisualizer
from family_tree.app.extensions import db
import traceback

person_service = None

def inject_service(service):
    global person_service
    person_service = service

def register_tree_routes(person_api):
    from family_tree.interfaces.forms.person_form import PersonForm
    @person_api.route("/visualize/tree/<int:person_id>", endpoint="visualize_tree_by_id")
    def person_get_family_tree():
        try:
            visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
            tree_data = visualizer.generate_familytree_data(root_person_id=1)
            return jsonify(tree_data)
        except Exception as e:
            current_app.logger.error(f"person_get_family_tree error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500


    @person_api.route("/visualize/tree/root")
    def get_root_tree():
        try:
            visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
            root_person_id = 1 
            tree_data = visualizer.generate_familytree_data(root_person_id)  
            return jsonify(tree_data)
        except Exception as e:
            traceback.print_exc()
            current_app.logger.error(f"Visualization root error: {str(e)}")
            return jsonify({'error': 'Server error'}), 500

    @person_api.route('/tree')
    def show_tree():
        visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
        tree_data = visualizer.generate_familytree_data(root_person_id=1)
        form = PersonForm()
        return render_template(
            'tree.html',
            form=form,
            nodes=tree_data['nodes'],
            edges=tree_data['edges'],
            person_id=1
        )

    @person_api.route('/visualize/tree/<int:person_id>')
    def visualize_tree(person_id):
        try:
            if person_id <= 0:
                abort(400, description="Invalid person ID")
            visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
            tree_data = visualizer.generate_familytree_data(person_id)
            if not tree_data["nodes"] and not tree_data["edges"]:
                return jsonify({'error': 'Person not found'}), 404
            return jsonify(tree_data)
        except Exception as e:
            traceback.print_exc()
            current_app.logger.error(f"Visualization error: {str(e)}")
            return jsonify({'error': 'Server error'}), 500

    @person_api.route('/tree/<int:person_id>', methods=['GET'])
    def show_tree_by_id(person_id):
        visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
        tree_data = visualizer.generate_familytree_data(root_person_id=person_id)
        form = PersonForm()  
        if current_app.config.get('TESTING'):
            return jsonify(tree_data)
        else:
            return render_template(
            'tree.html',
            form=form,
            nodes=tree_data['nodes'],
            edges=tree_data['edges'],
            person_id=person_id
        )

    @person_api.route('/tree')
    def api_tree_default():
        try:
            visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
            root_person_id = 1
            tree_data = visualizer.generate_familytree_data(root_person_id)
            return jsonify(tree_data)
        except Exception as e:
            traceback.print_exc()
            current_app.logger.error(f"API /tree error: {str(e)}")
            return jsonify({'error': 'Server error'}), 500

