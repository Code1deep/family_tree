# family_tree/interfaces/api/resources/tree/routes_tree_views.py

from flask import render_template, current_app
from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
from family_tree.infrastructure.visualization.tree_visualizer import FamilyTreeVisualizer
from family_tree.app.extensions import db


def register_tree_view_routes(bp):
    """
    Enregistre les routes Flask HTML (pages) liées à l'affichage de l'arbre.
    """

    @bp.route('/', methods=['GET'])
    def tree_index():
        return render_template('tree/index.html')

    @bp.route('/fullscreen', methods=['GET'])
    def tree_fullscreen():
        return render_template('tree/fullscreen.html')

    @bp.route('/<int:person_id>', methods=['GET'])
    def show_tree_by_id(person_id):
        """
        Affiche l’arbre généalogique à partir d’un ID donné, côté interface HTML.
        """
        visualizer = FamilyTreeVisualizer(current_app, PersonRepository(db.session))
        tree_data = visualizer.generate_familytree_data(root_person_id=person_id)
        from family_tree.interfaces.forms.person_form import PersonForm
        form = PersonForm()
        return render_template(
            'tree.html', form=form,
            nodes=tree_data['nodes'],
            edges=tree_data['edges']
        )
