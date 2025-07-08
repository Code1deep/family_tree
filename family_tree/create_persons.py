# family_tree/create_persons.py

from family_tree.app.extensions import db
from family_tree.domain.models.person import Person
from sqlalchemy import inspect

def create_persons_table():
    inspector = inspect(db.engine)
    if not inspector.has_table(Person.__tablename__):
        db.create_all()
        print(f"✅ Table '{Person.__tablename__}' créée.")
    else:
        print(f"ℹ️ Table '{Person.__tablename__}' existe déjà.")

