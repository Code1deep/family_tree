# interfaces/api/resources/tree/__init__.py

from flask import Blueprint

# Création du blueprint
tree_api = Blueprint('tree_api', __name__)

# Import des routes APRÈS la création du blueprint pour éviter les imports circulaires
from . import routes_tree_api
from . import init_tree_service

# Initialisation des routes
routes_tree_api.register_routes(tree_api)


