# family_tree/create_persons.py

from family_tree.app.extensions import db
from family_tree.domain.models.person import Person
from sqlalchemy import inspect

def create_persons_table():
    """
    Crée explicitement la table 'persons' si absente,
    en mode transactionnel atomique.
    """
    inspector = inspect(db.engine)
    if not inspector.has_table(Person.__tablename__):
        print("✅ Table 'persons' absente, création...")
        with db.engine.begin() as conn:
            Person.__table__.create(bind=conn, checkfirst=True)
        print("✅ Table 'persons' créée et transaction validée.")
    else:
        print("✅ Table 'persons' déjà présente.")



