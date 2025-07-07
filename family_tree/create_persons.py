# family_tree/database/create_persons.py
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.schema import CreateTable
from family_tree.domain.models.person import Person
from app.extensions import db

def create_persons_table():
    """
    Crée la table 'persons' avec toutes les colonnes définies dans Person
    sans insérer de données.
    """
    try:
        # Génère le SQL de création de table
        table_creation_sql = str(CreateTable(Person.__table__))
        
        # Exécute la création
        db.engine.execute(table_creation_sql)
        print("✓ Table 'persons' créée avec succès")
        
    except SQLAlchemyError as e:
        print(f"❌ Erreur lors de la création de la table: {str(e)}")
        raise
