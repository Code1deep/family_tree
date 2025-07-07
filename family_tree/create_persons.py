# family_tree/create_persons.py
from family_tree.app.factory import db  # <-- importe ton db directement
from family_tree.domain.models.person import Person

def create_persons_table():
    """Crée la table persons"""
    try:
        if not db.engine.dialect.has_table(db.engine, Person.__tablename__):
            db.create_all()
            print("✓ Table 'persons' créée avec succès")
        else:
            print("✓ Table 'persons' existe déjà")
    except Exception as e:
        print(f"❌ Erreur création table: {str(e)}")
        raise
