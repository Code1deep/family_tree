# family_tree/domain/services/__init__.py
from family_tree.app.extensions import db
from family_tree.domain.models.person import Person
from family_tree.domain.services.person_service import PersonService

__all__ = ['PersonService']
