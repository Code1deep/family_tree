# fix_names.py
"""
SCRIPT DEFINITIF - VIDER ET METTRE À JOUR LES NOMS
"""

from family_tree.app.extensions import db
from sqlalchemy import text, inspect

def fix_names():
    inspector = inspect(db.engine)

    if 'persons' not in inspector.get_table_names():
        print("❌ Table 'persons' absente. Abandon fix_names()")
        return

    # 1️⃣ Vérifier colonne full_name
    with db.engine.begin() as conn:
        conn.execute(text("""
            ALTER TABLE persons ADD COLUMN IF NOT EXISTS full_name TEXT
        """))
        print("🗂️ Colonne full_name vérifiée.")

    # 2️⃣ Vérifier colonne father_full_name
    with db.engine.begin() as conn:
        conn.execute(text("""
            ALTER TABLE persons ADD COLUMN IF NOT EXISTS father_full_name TEXT
        """))
        print("🗂️ Colonne father_full_name vérifiée.")

    # 3️⃣ Calculer full_name des pères eux-mêmes
    with db.engine.begin() as conn:
        conn.execute(text("""
            UPDATE persons
            SET full_name = first_name || ' ' || last_name
            WHERE full_name IS NULL OR full_name = ''
        """))
        print("🔄 Calcul full_name pères directs.")

    # 4️⃣ Calculer father_full_name pour chaque enfant
    with db.engine.begin() as conn:
        conn.execute(text("""
            UPDATE persons p
            SET father_full_name = f.full_name
            FROM persons f
            WHERE p.father_id = f.id
        """))
        print("🔄 Calcul father_full_name enfants.")

    # 5️⃣ Boucle pour calculer full_name enfants itérativement
    with db.engine.begin() as conn:
        updated = True
        while updated:
            result = conn.execute(text("""
                UPDATE persons p
                SET full_name = p.first_name || ' بْنُ ' || f.first_name
                FROM persons f
                WHERE p.father_id = f.id
                  AND (p.full_name IS NULL OR p.full_name = '')
                  AND f.full_name IS NOT NULL
                RETURNING p.id
            """))
            updated = result.rowcount > 0
            if updated:
                print(f"🔁 Itération boucle enfants : {result.rowcount} lignes mises à jour")

    print("✅ Tous les noms calculés !")

if __name__ == "__main__":
    fix_names()


