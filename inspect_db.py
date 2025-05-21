import sqlite3
from pprint import pprint

DB_PATH = 'instance/family.db'

def inspect_database():
    print("\n=== Inspection de la base de données ===")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Liste des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("\nTables existantes:")
        pprint(cursor.fetchall())
        
        # Schéma de la table persons
        cursor.execute("PRAGMA table_info(persons);")
        print("\nStructure de la table 'persons':")
        pprint(cursor.fetchall())
        
        # Données dans persons
        cursor.execute("SELECT * FROM persons;")
        print("\nDonnées dans 'persons':")
        pprint(cursor.fetchall())
        
    except Exception as e:
        print(f"\nErreur: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    inspect_database()