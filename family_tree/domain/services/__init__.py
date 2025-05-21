from setup_path import setup_sys_path
setup_sys_path(__file__)

from app.extensions import db
from domain.models.person import Person
from domain.services.person_service import PersonService

__all__ = ['PersonService']
