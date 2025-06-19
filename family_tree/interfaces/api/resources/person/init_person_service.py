# interfaces/api/resources/person/init_person_service.py
from family_tree.domain.services.person_service import PersonService
from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
from family_tree.interfaces.api.resources.person.routes_crud import register_crud_routes
from family_tree.interfaces.api.resources.person.routes_api import register_api_routes
from family_tree.interfaces.api.resources.person.routes_tree import register_tree_routes
from family_tree.interfaces.api.resources.person.routes_misc import register_misc_routes
from family_tree.interfaces.api.resources.person.blueprint import person_api

def init_person_resources(db_session):
    service = PersonService(PersonRepository(db_session))
    
    # Tu passes le service explicitement partout
    register_crud_routes(person_api)
    register_api_routes(person_api)
    register_tree_routes(person_api)
    register_misc_routes(person_api)

def create_person_api():
    return person_api

