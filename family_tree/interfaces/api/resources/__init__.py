from setup_path import setup_sys_path
setup_sys_path(__file__)

from interfaces.api.resources.person_resource import person_api

__all__ = ['person_api']