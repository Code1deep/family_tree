
from app.extensions import db  # Utilisez le db centralisé
from domain.models.person import Person

__all__ = ["Person"]  # db retiré car importé depuis extensions
