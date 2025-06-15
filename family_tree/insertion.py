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

            # Nettoyage éventuel
            if DB_PATH.exists():
                print("🧹 Suppression de l’ancienne base...")
                DB_PATH.unlink()

            db.create_all()
            print_all_persons("🕵️‍♂️ Juste après création (devrait être vide)")

            # Données à insérer
            family_members = [
                {'id': 2, 'first_name': 'Abu Talib', 'last_name': 'Ibn Abd al-Muttalib', 'gender': 'male'},
                {'id': 3, 'first_name': 'Fatima', 'last_name': 'bint Asad', 'gender': 'female'},
                {'id': 1, 'first_name': 'Ali', 'last_name': 'Ibn Abi Talib', 'gender': 'male',
                 'father_id': 2, 'mother_id': 3},
                {'id': 4, 'first_name': 'Hasan', 'last_name': 'Ibn Ali', 'gender': 'male',
                 'father_id': 1, 'mother_id': 3},
                {'id': 5, 'first_name': 'Hussein', 'last_name': 'Ibn Ali', 'gender': 'male',
                 'father_id': 1, 'mother_id': 3}
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

if __name__ == '__main__':
    initialize_data()
