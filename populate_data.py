# populate_data.py
from setup_path import setup_sys_path
setup_sys_path(__file__)

from app.factory import create_app
from app.extensions import db
from domain.models.person import Person

def seed():
    app = create_app("app.config.DevelopmentConfig")
    with app.app_context():
        db.drop_all()
        db.create_all()

        grandfather1 = Person(
            first_name="عبدالله", last_name="الفهيد", birth_date="1800-01-01", birth_place="نجد"
        )
        grandfather2 = Person(
            first_name="محمد", last_name="السديري", birth_date="1805-01-01", birth_place="الرياض"
        )

        db.session.add_all([grandfather1, grandfather2])
        db.session.commit()

        # Requête pour obtenir leur ID
        gf1_id = grandfather1.id

        sons = [
            Person(first_name="خالد", last_name="الفهيد", father_id=gf1_id, birth_date="1825-01-01", birth_place="الرياض",
                   gender="male", residence="الرياض", alive=True, known_enemies="لا", fitan="لا", death_reason=None),
            Person(first_name="علي", last_name="الفهيد", father_id=gf1_id, birth_date="1830-01-01", birth_place="الرياض",
                   gender="male", residence="الرياض", alive=False, death_date="1890-01-01", died_in_battle=True, death_reason="معركة"),
            Person(first_name="فهد", last_name="الفهيد", father_id=gf1_id, birth_date="1835-01-01", birth_place="الرياض",
                   gender="male", residence="الرياض", alive=True, notes="ذو نفوذ كبير")
        ]

        db.session.add_all(sons)
        db.session.commit()
        print("✓ Base de données peuplée avec succès.")

if __name__ == '__main__':
    seed()
