# interfaces/api/resources/person/__init__.py

from family_tree.interfaces.api.resources.person.routes_crud import register_crud_routes
from family_tree.interfaces.api.resources.person.routes_api import register_api_routes
from family_tree.interfaces.api.resources.person.routes_tree import register_tree_routes
from family_tree.interfaces.api.resources.person.routes_misc import register_misc_routes
from family_tree.interfaces.api.resources.person.blueprint import person_api

register_crud_routes(person_api)
register_api_routes(person_api)
register_tree_routes(person_api)
register_misc_routes(person_api)

__all__ = ['person_api']



