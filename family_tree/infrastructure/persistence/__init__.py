# family_tree/infrastructure/persistence/__init__.py
from family_tree.app.extensions import db  # Utilisez le db centralisé
from family_tree.domain.models.person import Person

__all__ = ["Person"]  # db retiré car importé depuis extensions
