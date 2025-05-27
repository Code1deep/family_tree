# interfaces/api/resources/person/init_person_service.py

from family_tree.domain.services.person_service import PersonService
from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
from family_tree.interfaces.api.resources.person.routes_api import inject_service
from family_tree.interfaces.api.resources.person.blueprint import person_api

def init_person_resources(db_session):
    repo = PersonRepository(db_session)
    service = PersonService(repo)
    inject_service(service)

def create_person_api():
    return person_api


