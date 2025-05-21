# C:\family_tree\insersion.py
# insersion.py
from app.factory import create_app
from app.extensions import db
from domain.models.person import Person
from sqlalchemy.exc import IntegrityError

app = create_app()

def safe_insert_person(person_data):
    """Insertion sécurisée avec gestion des erreurs"""
    with app.app_context():
        try:
            # Vérifie les parents existants
            if 'father_id' in person_data and person_data['father_id']:
                if not db.session.get(Person, person_data['father_id']):
                    raise ValueError(f"Père ID {person_data['father_id']} inexistant")
            
            if 'mother_id' in person_data and person_data['mother_id']:
                if not db.session.get(Person, person_data['mother_id']):
                    raise ValueError(f"Mère ID {person_data['mother_id']} inexistante")
            
            # Insertion ou mise à jour
            person = db.session.get(Person, person_data['id'])
            if person:
                for key, value in person_data.items():
                    setattr(person, key, value)
            else:
                person = Person(**person_data)
            
            db.session.add(person)
            db.session.commit()
            return person
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Violation d'intégrité (ID peut-être dupliqué)")
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Erreur lors de l'insertion: {str(e)}")

def insert_sample_data():
    """Peuplement initial optimisé"""
    sample_data = [
        {'id': 2, 'first_name': 'Abu Talib', 'last_name': 'Ibn Abd al-Muttalib', 'gender': 'male'},
        {'id': 3, 'first_name': 'Fatima', 'last_name': 'Bint Asad', 'gender': 'female'},
        {'id': 1, 'first_name': 'Ali', 'last_name': 'Ibn Abi Talib', 'gender': 'male', 
         'father_id': 2, 'mother_id': 3},
        {'id': 4, 'first_name': 'Hasan', 'last_name': 'Ibn Ali', 'gender': 'male',
         'father_id': 1, 'mother_id': 3},
        {'id': 5, 'first_name': 'Hussein', 'last_name': 'Ibn Ali', 'gender': 'male',
         'father_id': 1, 'mother_id': 3}
    ]
    
    with app.app_context():
        try:
            for data in sample_data:
                safe_insert_person(data)
            print("Données insérées avec succès")
        except ValueError as e:
            print(f"Erreur: {str(e)}")

if __name__ == '__main__':
    insert_sample_data()