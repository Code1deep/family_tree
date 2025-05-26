# interfaces/api/resources/person/__init__.py
from .init_person_service import init_person_resources

from flask import Blueprint
from family_tree.interfaces.api.resources.person.routes_crud import register_crud_routes
from family_tree.interfaces.api.resources.person.routes_api import register_api_routes
from family_tree.interfaces.api.resources.person.routes_tree import register_tree_routes
from family_tree.interfaces.api.resources.person.routes_misc import register_misc_routes
from family_tree.interfaces.api.resources.person.init_person_service import init_resources, create_person_api

person_api = Blueprint('person_api', __name__)

register_crud_routes(person_api)
register_api_routes(person_api)
register_tree_routes(person_api)
register_misc_routes(person_api)

# Export explicite des fonctions nécessaires
__all__ = ['person_api', 'init_person_resources']
