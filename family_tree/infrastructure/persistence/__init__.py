from setup_path import setup_sys_path
setup_sys_path(__file__)

from app.extensions import db  # Utilisez le db centralisé
from domain.models.person import Person

__all__ = ["Person"]  # db retiré car importé depuis extensions