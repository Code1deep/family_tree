import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuration de base
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "instance" / "family.db"
os.makedirs(DB_PATH.parent, exist_ok=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import des modèles après configuration
from family_tree.app.extensions import db
from family_tree.domain.models.person import Person

db.init_app(app)

def print_all_persons(msg="📋 Contenu actuel"):
    persons = Person.query.order_by(Person.id).all()
    print(f"\n{msg} ({len(persons)} personnes):")
    for p in persons:
        parents = f" (parents: {p.father_id}/{p.mother_id})" if p.father_id or p.mother_id else ""
        print(f"  - {p.id}: {p.full_name}{parents}")

def initialize_data():
    with app.app_context():
        try:
            if DB_PATH.exists():
                print("ℹ️ Base existante détectée")
                return False

            family_members = [
                # Niveau 0
                {'id': 2, 'first_name': 'Abu Talib', 'last_name': 'Ibn Abd al-Muttalib', 'gender': 'male'},
                {'id': 3, 'first_name': 'Fatima', 'last_name': 'bint Asad', 'gender': 'female'},
                
                # Niveau 1
                {'id': 1, 'first_name': 'Ali', 'last_name': 'Ibn Abi Talib', 'gender': 'male',
                 'father_id': 2, 'mother_id': 3},
                
                # Niveau 2
                {'id': 4, 'first_name': 'Hasan', 'last_name': 'Ibn Ali', 'gender': 'male',
                 'father_id': 1, 'mother_id': 3},
                {'id': 5, 'first_name': 'Hussein', 'last_name': 'Ibn Ali', 'gender': 'male',
                 'father_id': 1, 'mother_id': 3}
            ]

            db.create_all()
            for member in family_members:
                db.session.add(Person(**member))
            db.session.commit()
            
            print("✅ Niveaux 0-2 initialisés (5 personnes)")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur initialisation: {str(e)}")
            return False

def add_level_3():
    with app.app_context():
        try:
            # Vérifie si le niveau 3 existe déjà
            if Person.query.filter(Person.id.in_([6,7])).count() >= 2:
                print("ℹ️ Niveau 3 déjà existant")
                return False

            new_members = [
                {'id': 6, 'first_name': 'Abdullah', 'last_name': 'Ibn Hasan', 'gender': 'male',
                 'father_id': 4, 'mother_id': None},
                {'id': 7, 'first_name': 'Fatima', 'last_name': 'bint Hasan', 'gender': 'female',
                 'father_id': 4, 'mother_id': None}
            ]

            for member in new_members:
                db.session.add(Person(**member))
            db.session.commit()
            
            print("✅ Niveau 3 ajouté (2 nouvelles personnes)")
            print_all_persons("État après ajout")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur niveau 3: {str(e)}")
            return False

def add_level_4():
    with app.app_context():
        try:
            # Vérifie si le niveau 4 existe déjà
            if Person.query.filter(Person.id.in_([8,9])).count() >= 2:
                print("ℹ️ Niveau 4 déjà existant")
                return False

            new_members = [
                {'id': 8, 'first_name': 'Ali', 'last_name': 'Ibn Abdullah', 'gender': 'male',
                 'father_id': 6, 'mother_id': None},
                {'id': 9, 'first_name': 'Zaynab', 'last_name': 'bint Abdullah', 'gender': 'female',
                 'father_id': 6, 'mother_id': None}
            ]

            for member in new_members:
                db.session.add(Person(**member))
            db.session.commit()
            
            print("✅ Niveau 4 ajouté (2 nouvelles personnes)")
            print_all_persons("État après ajout")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur niveau 4: {str(e)}")
            return False

def main():
    print("\n=== Initialisation de l'arbre généalogique ===")
    
    if not DB_PATH.exists():
        if not initialize_data():
            return
    
    print("\nOptions disponibles:")
    print("1. Ajouter le niveau 3 (enfants de Hasan)")
    print("2. Ajouter le niveau 4 (enfants de Abdullah)")
    print("3. Afficher l'arbre actuel")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    if choice == "1":
        add_level_3()
    elif choice == "2":
        add_level_3()  # Pré-requis
        add_level_4()
    elif choice == "3":
        print_all_persons("Arbre actuel")
    else:
        print("Option invalide")

if __name__ == '__main__':
    main()
