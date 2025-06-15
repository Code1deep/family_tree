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

            # 1. Crée les parents initiaux (sans parents eux-mêmes)
            ancestors = [
                {'id': 2, 'first_name': 'Abu Talib', 'last_name': 'Ibn Abd al-Muttalib', 'gender': 'male'},
                {'id': 3, 'first_name': 'Fatima', 'last_name': 'bint Asad', 'gender': 'female'}
            ]

            # 2. Crée la racine principale (Ali)
            root = {
                'id': 1, 
                'first_name': 'Ali', 
                'last_name': 'Ibn Abi Talib', 
                'gender': 'male',
                'father_id': 2, 
                'mother_id': 3
            }

            # 3. Génération des 4 niveaux descendants (total 5 niveaux)
            family_members = ancestors + [root]
            current_id = 10  # Commence après les IDs existants

            def add_children(parent_id, level):
                nonlocal current_id
                if level >= 5:  # S'arrête au 5ème niveau
                    return []
                
                children = []
                for i in range(2):  # 2 enfants par nœud
                    child = {
                        'id': current_id,
                        'first_name': f'Enfant-{current_id}',
                        'last_name': f'de-{parent_id}',
                        'gender': 'male' if current_id % 2 else 'female',
                        'father_id': parent_id if parent_id % 2 else None,
                        'mother_id': parent_id if not parent_id % 2 else None
                    }
                    children.append(child)
                    current_id += 1
                    
                    # Ajoute récursivement les enfants des enfants
                    children.extend(add_children(child['id'], level + 1))
                return children

            # Génère l'arbre complet
            family_members.extend(add_children(root['id'], 1))

            # Insertion en base
            for member in family_members:
                db.session.add(Person(**member))

            db.session.commit()
            print(f"✅ {len(family_members)} membres insérés!")
            print_all_persons("📦 Arbre final")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur: {str(e)}")

if __name__ == '__main__':
    initialize_data()
