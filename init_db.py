from setup_path import setup_sys_path
setup_sys_path(__file__)

from app.app import create_app
from domain.models import Person

def init_db():
    app = create_app()
    with app.app_context():
        from family_tree.extensions import db
        
        # Supprime et recrée toutes les tables
        db.drop_all()
        db.create_all()
        
        # Ajoute un utilisateur test
        if Person.query.count() == 0:
            test_person = Person(
                first_name="Test",
                last_name="User",
                gender="male"
            )
            db.session.add(test_person)
            db.session.commit()
            print("Base de données initialisée avec un enregistrement test")

if __name__ == '__main__':
    init_db()