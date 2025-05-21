import os
from app import create_app
from app.extensions import db

def reset_database():
    app = create_app()
    
    with app.app_context():
        # Suppression de l'ancienne base
        db_path = os.path.join(app.instance_path, 'family.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Ancienne base de données supprimée")
        
        # Création des tables
        db.create_all()
        print("Nouvelle base de données créée avec succès!")

if __name__ == '__main__':
    reset_database()