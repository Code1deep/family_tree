# scripts/seed_and_check.py

from family_tree.app import create_app
from family_tree.database import db
from family_tree.domain.models.person import Person
from family_tree.insertion import full_initialize

app = create_app()

with app.app_context():
    # Combien avant ?
    count_before = Person.query.count()
    print(f"🔍 AVANT SEED : {count_before} personnes")

    # Si vide → on peuple
    if count_before == 0:
        full_initialize()
        db.session.commit()
        print("✅ full_initialize() exécuté")

    # Combien après ?
    count_after = Person.query.count()
    print(f"🔍 APRÈS SEED : {count_after} personnes")
