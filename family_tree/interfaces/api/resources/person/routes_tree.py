 # routes_tree.py
from .routes_crud import person_api  # Réutilisation du même blueprint

@person_api.route('/tree')
def show_tree():
    from infrastructure.persistence.repositories.person_repo import PersonRepository
    visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
    tree_data = visualizer.generate_familytree_data()
    return render_template('tree.html', nodes=tree_data['nodes'], edges=tree_data['edges'])

@person_api.route('/api/visualize/tree/<int:person_id>')
def visualize_tree(person_id):
    try:
        if person_id <= 0:
            abort(400, description="Invalid person ID")
        from infrastructure.persistence.repositories.person_repo import PersonRepository
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
