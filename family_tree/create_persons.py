# family_tree/create_persons.py
from flask import current_app
from family_tree.domain.models.person import Person

def create_persons_table():
    """Crée la table persons dans le contexte applicatif"""
    try:
        # Utilise db depuis current_app.extensions
        db = current_app.extensions['sqlalchemy'].db
        
        # Vérifie si la table existe déjà
        if not db.engine.dialect.has_table(db.engine, Person.__tablename__):
            db.create_all()
            print("✓ Table 'persons' créée avec succès")
        else:
            print("✓ Table 'persons' existe déjà")
    except Exception as e:
        print(f"❌ Erreur création table: {str(e)}")
        raise
