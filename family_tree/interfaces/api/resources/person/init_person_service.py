# interfaces/api/resources/person/init_person_service.py

from family_tree.domain.services.person_service import PersonService
from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
from family_tree.app.extensions import db

person_service = None

def init_resources(db_session):
    global person_service
    repo = PersonRepository(db_session)
    person_service = PersonService(repo)

# ------------ INIT POUR INJECTION DE SERVICE (tests) -----------
def create_person_api(service):
    global person_service
    person_service = service
    return person_api

init_resources(db.session)
