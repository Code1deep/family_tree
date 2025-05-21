# infrastructure/visualization/views.py
from setup_path import setup_sys_path
setup_sys_path(__file__)

#from flask import Blueprint, current_app, jsonify
#from infrastructure.visualization.tree_visualizer import FamilyTreeVisualizer
#from domain.models.person import Person  # Import absolu maintenant fonctionnel

from flask import Flask
from interfaces.api.resources.tree_resource import tree_api
from interfaces.api.resources.person_resource import person_api

def register_blueprints(app: Flask):
    """Enregistre tous les Blueprints API"""
    app.register_blueprint(person_api)
    app.register_blueprint(tree_api)



#vis_bp = Blueprint('visualization', __name__)

#@vis_bp.route('/api/visualize/tree/<int:person_id>')
#def visualize_tree(person_id):
    #try:
        #visualizer = FamilyTreeVisualizer(current_app)
        #tree_data = visualizer.generate_familytree_data(person_id)
        #return jsonify(tree_data if tree_data else {'error': 'Person not found'})
    #except Exception as e:
        #current_app.logger.error(f"Visualization error: {str(e)}")
        #return jsonify({'error': 'Server error'}), 500
    
#@vis_bp.route('/test')
#def test():
    #return "L'application fonctionne 🎉"


