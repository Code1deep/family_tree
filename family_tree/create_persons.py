# family_tree/database/create_persons.py
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.schema import CreateTable
from family_tree.domain.models.person import Person

def create_persons_table():
    """Crée uniquement la table persons basée sur le modèle existant"""
    try:
        # Vérifie si la table existe déjà
        if not db.engine.dialect.has_table(db.engine, Person.__tablename__):
            Person.__table__.create(db.engine)
            print("✓ Table 'persons' créée avec succès")
        else:
            print("✓ Table 'persons' existe déjà")
    except Exception as e:
        print(f"❌ Erreur création table: {str(e)}")
        raise
