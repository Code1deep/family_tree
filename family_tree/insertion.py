# family_tree/insertion.py 

import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 📌 Chemin de la base de données
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "instance" / "family.db"
os.makedirs(DB_PATH.parent, exist_ok=True)

# 📦 App Flask temporaire pour initialiser le contexte
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'timeout': 30,
        'check_same_thread': False,
        'uri': True
    }
}

# 🔁 Import après configuration
from family_tree.app.extensions import db
from family_tree.domain.models.person import Person

db.init_app(app)

def print_all_persons(msg="📋 Contenu actuel de la base"):
    persons = Person.query.all()
    print(f"\n{msg} ({len(persons)} entrées) :")
    for p in persons:
        print(f"  - {p.id}: {p.full_name} (gender: {p.gender})")

def initialize_data():
    with app.app_context():
        try:
            if db.session.query(Person).count() > 0:
                print("ℹ️ Base déjà peuplée.")
                return

            family_members = [
                # Niveau 0 (ancêtres)
                {'id': 2, 'first_name': 'Abu Talib', 'last_name': 'Ibn Abd al-Muttalib', 'gender': 'male'},
                {'id': 3, 'first_name': 'Fatima', 'last_name': 'bint Asad', 'gender': 'female'},
                
                # Niveau 1 (racine)
                {'id': 1, 'first_name': 'Ali', 'last_name': 'Ibn Abi Talib', 'gender': 'male',
                 'father_id': 2, 'mother_id': 3},
                
                # Niveau 2 (enfants)
                {'id': 4, 'first_name': 'Hasan', 'last_name': 'Ibn Ali', 'gender': 'male',
                 'father_id': 1, 'mother_id': None},  # Mère non spécifiée
                {'id': 5, 'first_name': 'Hussein', 'last_name': 'Ibn Ali', 'gender': 'male',
                 'father_id': 1, 'mother_id': None}
            ]


            for member in family_members:
                db.session.add(Person(**member))

            db.session.commit()
            print("✅ Données insérées avec succès!")
            print_all_persons("📦 Après insertion")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur critique: {str(e)}")
            if DB_PATH.exists():
                print(f"Taille du fichier DB: {DB_PATH.stat().st_size} octets")

def add_level_3():
    with app.app_context():
        try:
            # Enfants de Hasan (niveau 3)
            new_members = [
                {'id': 6, 'first_name': 'Abdullah', 'last_name': 'Ibn Hasan', 'gender': 'male',
                 'father_id': 4, 'mother_id': None},
                {'id': 7, 'first_name': 'Fatima', 'last_name': 'bint Hasan', 'gender': 'female',
                 'father_id': 4, 'mother_id': None}
            ]

            for member in new_members:
                if not Person.query.get(member['id']):  # Évite les doublons
                    db.session.add(Person(**member))

            db.session.commit()
            print("✅ 2 nouveaux membres ajoutés (niveau 3)")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur: {str(e)}")

    # Niveau 4 (à exécuter après)
def add_level_4():
    with app.app_context():
        try:
            new_members2 = [
                {'id': 8, 'first_name': 'Ali', 'last_name': 'Ibn Abdullah', 'gender': 'male',
                 'father_id': 6, 'mother_id': None},
                {'id': 9, 'first_name': 'Zaynab', 'last_name': 'bint Abdullah', 'gender': 'female',
                 'father_id': 6, 'mother_id': None}
            ]
            for member in new_members2:
                if not Person.query.get(member['id']):  # Évite les doublons
                    db.session.add(Person(**member))

            db.session.commit()
            print("✅ 2 nouveaux membres ajoutés (niveau 4)")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur: {str(e)}")


if __name__ == '__main__':
    initialize_data()  # Initialise les niveaux 0-2 (5 insertions)
    add_level_3()      # Ajoute le niveau 3 (2 nouvelles insertions)
    add_level_4()      # Ajoute le niveau 4 (2 nouvelles insertions)
