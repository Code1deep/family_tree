# interfaces/api/resources/tree/__init__.py

from flask import Blueprint

# Création du blueprint
tree_api = Blueprint('tree_api', __name__)

# Import des routes APRÈS la création du blueprint pour éviter les imports circulaires
#from . import routes_tree_api
from .init_tree_service import init_tree_resources

# Initialisation des routes
# routes_tree_api.register_routes(tree_api)


