# family_tree/database/create_persons.py

from app.extensions import db 
from family_tree.domain.models.person import Person

def create_persons_table():
    """Crée uniquement la table persons en utilisant les imports existants"""
    try:
        # Solution 1 (simple) - Utilise db.create_all()
        db.create_all()  # Crée toutes les tables non existantes
        
        # Solution 2 (alternative) - Création contrôlée
        # if not db.engine.dialect.has_table(db.engine, Person.__tablename__):
        #     Person.__table__.create(db.engine)
        
        print("✓ Table 'persons' créée avec succès")
    except Exception as e:
        print(f"❌ Erreur création table: {str(e)}")
        raise
