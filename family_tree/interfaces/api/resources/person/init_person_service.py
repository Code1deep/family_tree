#init_person_service.py


# person_api = Blueprint('person_api', __name__)
person_service = None

def init_resources(db_session):
    global person_service
    from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
    repo = PersonRepository(db_session)
    person_service = PersonService(repo)

# ------------ INIT POUR INJECTION DE SERVICE (tests) -----------

def create_person_api(service):
    global person_service
    person_service = service
    return person_api
