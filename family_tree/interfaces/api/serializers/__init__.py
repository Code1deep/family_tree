from setup_path import setup_sys_path
setup_sys_path(__file__)

from interfaces.api.serializers.person_serializer import PersonSerializer  # Export unique

__all__ = ['PersonSerializer']  # Rend explicite ce qui est exposé