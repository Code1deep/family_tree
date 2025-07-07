# family_tree/create_persons.py
from sqlalchemy import inspect
from family_tree.app.factory import db
from family_tree.domain.models.person import Person

def create_persons_table():
    """Crée la table persons dans le contexte applicatif"""
    try:
        inspector = inspect(db.engine)
        if not inspector.has_table(Person.__tablename__):
            db.create_all()
            print("✓ Table 'persons' créée avec succès")
        else:
            print("✓ Table 'persons' existe déjà")
    except Exception as e:
        print(f"❌ Erreur création table: {str(e)}")
        raise
