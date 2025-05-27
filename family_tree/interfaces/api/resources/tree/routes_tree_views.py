#  interfaces/api/resources/tree/routes_tree_views.py

# interfaces/api/resources/tree/routes_tree_views.py

from flask import render_template

def register_tree_view_routes(bp):
    """
    Enregistre les routes Flask HTML (pages) liées à l'affichage de l'arbre.
    """
    @bp.route('/')
    def tree_index():
        return render_template('tree/index.html')

    @bp.route('/fullscreen')
    def tree_fullscreen():
        return render_template('tree/fullscreen.html')
