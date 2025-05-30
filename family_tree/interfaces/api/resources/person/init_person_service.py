# interfaces/api/resources/person/init_person_service.py
from family_tree.domain.services.person_service import PersonService
from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository

# Import des injecteurs uniquement (pas de blueprint ici)
from family_tree.interfaces.api.resources.person.routes_api import inject_service as inject_api
from family_tree.interfaces.api.resources.person.routes_crud import inject_service as inject_crud
from family_tree.interfaces.api.resources.person.routes_tree import inject_service as inject_tree
from family_tree.interfaces.api.resources.person.routes_misc import inject_service as inject_misc

from family_tree.interfaces.api.resources.person.blueprint import person_api

def init_person_resources(db_session):
    service = PersonService(PersonRepository(db_session))
    inject_api(service)
    inject_crud(service)
    inject_tree(service)
    inject_misc(service)

def create_person_api():
    from family_tree.interfaces.api.resources.person.routes_tree import register_tree_routes
    register_tree_routes(person_api)
    return person_api

