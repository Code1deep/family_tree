from setup_path import setup_sys_path
setup_sys_path(__file__)

from infrastructure.persistence.repositories.person_repo import PersonRepository

__all__ = ['PersonRepository']