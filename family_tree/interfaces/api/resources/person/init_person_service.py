# interfaces/api/resources/person/init_person_service.py
from family_tree.domain.services.person_service import PersonService
from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
from family_tree.interfaces.api.resources.person.routes_api import inject_service as inject_api, register_api_routes
from family_tree.interfaces.api.resources.person.routes_crud import inject_service as inject_crud, register_crud_routes
from family_tree.interfaces.api.resources.person.routes_tree import inject_service as inject_tree, register_tree_routes
from family_tree.interfaces.api.resources.person.routes_misc import inject_service as inject_misc, register_misc_routes
from family_tree.interfaces.api.resources.person.blueprint import person_api

def init_person_resources(db_session):
    # Création d'une seule instance de service
    service = PersonService(PersonRepository(db_session))
    
    # Injection dans toutes les routes
    inject_api(service)
    inject_crud(service)
    inject_tree(service)
    inject_misc(service)
    
    # Enregistrement des routes (une seule fois)
    register_api_routes(person_api)
    register_crud_routes(person_api)
    register_tree_routes(person_api)
    register_misc_routes(person_api)

def create_person_api():
    return person_api
