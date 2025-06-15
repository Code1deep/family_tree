# C:\family_tree\insertion.py
import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuration absolue des chemins
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "instance" / "family.db"
os.makedirs(BASE_DIR / "instance", exist_ok=True)

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
# Import APRÈS la configuration de l'app
from app.extensions import db
db.init_app(app)  # Initialisation explicite
# Import du modèle enrichi
from family_tree.domain.models.person import Person

def print_all_persons(msg="📋 Contenu actuel de la base"):
    persons = Person.query.all()
    print(f"\n{msg} ({len(persons)} entrées) :")
    for p in persons:
        print(f"  - {p.id}: {p.full_name} (gender: {p.gender})")

def initialize_data():
    with app.app_context():
        try:
            print(f"\n🔧 Préparation de la base à: {DB_PATH}")

            if DB_PATH.exists():
                print("🧹 Suppression de l'ancienne base...")
                DB_PATH.unlink()

            db.create_all()

            # Fonction récursive pour générer l'arbre
            def create_family_tree(parent_id, current_level, max_level=5):
                if current_level > max_level:
                    return []
                
                members = []
                # Crée 2 enfants pour chaque parent
                for i in range(1, 3):
                    child_id = parent_id * 10 + i
                    child = {
                        'id': child_id,
                        'first_name': f'Prénom-{child_id}',
                        'last_name': f'Nom-{child_id}',
                        'gender': 'male' if child_id % 2 else 'female',
                        'father_id': parent_id if parent_id % 2 else None,
                        'mother_id': parent_id if not parent_id % 2 else None
                    }
                    members.append(child)
                    # Appel récursif pour les niveaux suivants
                    members.extend(create_family_tree(child_id, current_level + 1, max_level))
                
                return members

            # Racine de l'arbre (Ali Ibn Abi Talib)
            root_member = {
                'id': 1,
                'first_name': 'Ali',
                'last_name': 'Ibn Abi Talib',
                'gender': 'male',
                'father_id': None,
                'mother_id': None
            }

            # Génération de l'arbre complet
            family_members = [root_member] + create_family_tree(1, 2)  # Niveau 1 = racine

            # Ajout des parents initiaux (optionnel)
            family_members.extend([
                {'id': 2, 'first_name': 'Abu Talib', 'last_name': 'Ibn Abd al-Muttalib', 'gender': 'male'},
                {'id': 3, 'first_name': 'Fatima', 'last_name': 'bint Asad', 'gender': 'female'}
            ])
            root_member['father_id'] = 2
            root_member['mother_id'] = 3

            # Insertion en base
            for member in family_members:
                db.session.add(Person(**member))

            db.session.commit()
            print(f"✅ {len(family_members)} membres insérés avec succès!")
            print_all_persons("📦 Arbre final")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur: {str(e)}")

if __name__ == '__main__':
    initialize_data()
