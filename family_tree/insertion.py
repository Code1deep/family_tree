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
    persons = Person.query.order_by(Person.id).all()
    print(f"\n{msg} ({len(persons)} entrées) :")
    for p in persons:
        print(f"  - {p.id}: {p.full_name} (gender: {p.gender})")

def initialize_data():
    with app.app_context():
        try:
            if db.session.query(Person).count() > 0:
                print("ℹ️ Base déjà peuplée.")
                print_all_persons("État actuel")
                return

            family_members = [
                {'id': 2, 'first_name': 'Abu Talib', 'last_name': 'Ibn Abd al-Muttalib', 'gender': 'male'},
                {'id': 3, 'first_name': 'Fatima', 'last_name': 'bint Asad', 'gender': 'female'},
                {'id': 1, 'first_name': 'Ali', 'last_name': 'Ibn Abi Talib', 'gender': 'male',
                 'father_id': 2, 'mother_id': 3},
                {'id': 4, 'first_name': 'Hasan', 'last_name': 'Ibn Ali', 'gender': 'male',
                 'father_id': 1},
                {'id': 5, 'first_name': 'Hussein', 'last_name': 'Ibn Ali', 'gender': 'male',
                 'father_id': 1}
            ]

            for member in family_members:
                db.session.add(Person(**member))

            db.session.commit()
            print("✅ Données niveaux 0-2 insérées avec succès!")
            print_all_persons("Après insertion niveaux 0-2")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur insertion niveaux 0-2: {str(e)}")

def add_level_3():
    with app.app_context():
        try:
            existing = Person.query.filter(Person.id.in_([6,7])).all()
            print(f"🔍 Niveau 3 : {len(existing)} personne(s) déjà présentes : {[p.id for p in existing]}")
            if existing:
                print("ℹ️ Le niveau 3 existe déjà")
                return

            new_members = [
                {'id': 6, 'first_name': 'Abdullah', 'last_name': 'Ibn Hasan',
                 'gender': 'male', 'father_id': 4},
                {'id': 7, 'first_name': 'Fatima', 'last_name': 'bint Hasan',
                 'gender': 'female', 'father_id': 4}
            ]

            for member in new_members:
                if not Person.query.get(member['id']):
                    db.session.add(Person(**member))

            db.session.commit()
            print("✅ Niveau 3 ajouté avec succès!")
            print_all_persons("Après ajout niveau 3")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur niveau 3: {str(e)}")

def add_level_4():
    with app.app_context():
        try:
            existing = Person.query.filter(Person.id.in_([8,9])).all()
            print(f"🔍 Niveau 4 : {len(existing)} personne(s) déjà présentes : {[p.id for p in existing]}")
            if existing:
                print("ℹ️ Le niveau 4 existe déjà")
                return

            new_members = [
                {'id': 8, 'first_name': 'Ali', 'last_name': 'Ibn Abdullah',
                 'gender': 'male', 'father_id': 6},
                {'id': 9, 'first_name': 'Zaynab', 'last_name': 'bint Abdullah',
                 'gender': 'female', 'father_id': 6}
            ]

            for member in new_members:
                if not Person.query.get(member['id']):
                    db.session.add(Person(**member))

            db.session.commit()
            print("✅ Niveau 4 ajouté avec succès!")
            print_all_persons("Après ajout niveau 4")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur niveau 4: {str(e)}")

if __name__ == '__main__':
    print("\n=== Initialisation de l'arbre ===")
    print("\n=== Initialisation de l'arbre2 ===")
    print("\n=== Initialisation de l'arbre 3 ===")
    initialize_data()
    
    print("\n=== Ajout des niveaux supplémentaires ===")
    print("1. Ajouter uniquement le niveau 3")
    print("2. Ajouter les niveaux 3 et 4")
    choice = input("Votre choix (1-2): ").strip()

    if choice == "1":
        add_level_3()
    elif choice == "2":
        add_level_3()
        add_level_4()
    else:
        print("Option invalide")
