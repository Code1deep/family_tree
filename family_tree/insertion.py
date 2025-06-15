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

# 🔁 Import après config
from family_tree.app.extensions import db
from family_tree.domain.models.person import Person

db.init_app(app)

def print_all_persons(msg="📋 Contenu actuel de la base"):
    persons = Person.query.all()
    print(f"\n{msg} ({len(persons)} entrées) :")
    for p in persons:
        print(f"  - {p.id}: {p.full_name} (gender: {p.gender})")

def initialize_data():
    if db.session.query(Person).count() > 0:
        print("ℹ️ Base déjà peuplée.")
        return

    family_members = [
        {'id': 2, 'first_name': 'Abu Talib', 'last_name': 'Ibn Abd al-Muttalib', 'gender': 'male'},
        {'id': 3, 'first_name': 'Fatima', 'last_name': 'bint Asad', 'gender': 'female'},
        {'id': 1, 'first_name': 'Ali', 'last_name': 'Ibn Abi Talib', 'gender': 'male', 'father_id': 2, 'mother_id': 3},
        {'id': 4, 'first_name': 'Hasan', 'last_name': 'Ibn Ali', 'gender': 'male', 'father_id': 1},
        {'id': 5, 'first_name': 'Hussein', 'last_name': 'Ibn Ali', 'gender': 'male', 'father_id': 1}
    ]

    for member in family_members:
        db.session.add(Person(**member))
    db.session.commit()
    print("✅ Données niveaux 0-2 insérées avec succès!")
    print_all_persons("Après insertion niveaux 0-2")

def add_level_3():
    if Person.query.get(4) is None:
        print("❌ Hasan (ID 4) non trouvé, vérifiez les niveaux 0-2")
        return

    if Person.query.filter(Person.id.in_([6, 7])).count() > 0:
        print("ℹ️ Niveau 3 déjà présent")
        return

    new_members = [
        {'id': 6, 'first_name': 'Abdullah', 'last_name': 'Ibn Hasan', 'gender': 'male', 'father_id': 4},
        {'id': 7, 'first_name': 'Fatima', 'last_name': 'bint Hasan', 'gender': 'female', 'father_id': 4}
    ]

    for member in new_members:
        db.session.add(Person(**member))
    db.session.commit()
    print("✅ Niveau 3 ajouté")
    print_all_persons("État après niveau 3")

def add_level_4():
    if Person.query.get(6) is None:
        print("❌ Abdullah (ID 6) non trouvé, ajoutez niveau 3 d'abord")
        return

    if Person.query.filter(Person.id.in_([8, 9])).count() > 0:
        print("ℹ️ Niveau 4 déjà présent")
        return

    new_members = [
        {'id': 8, 'first_name': 'Ali', 'last_name': 'Ibn Abdullah', 'gender': 'male', 'father_id': 6},
        {'id': 9, 'first_name': 'Zaynab', 'last_name': 'bint Abdullah', 'gender': 'female', 'father_id': 6}
    ]

    for member in new_members:
        db.session.add(Person(**member))
    db.session.commit()
    print("✅ Niveau 4 ajouté")
    print_all_persons("État après niveau 4")

def full_initialize():
    with app.app_context():
        initialize_data()
        add_level_3()
        add_level_4()

# ✅ Tu peux appeler full_initialize() depuis ton serveur Flask ou ton script principal.
if __name__ == '__main__':
    print("\n=== appeler full_initialize() depuis ton serveur Flask ou ton script principal ===")
    full_initialize()
