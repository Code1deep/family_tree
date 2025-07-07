# fix_names.py
"""
SCRIPT DEFINITIF - VIDER ET METTRE À JOUR LES NOMS
"""

from sqlalchemy import create_engine, text

DB_URL = "postgresql://neondb_owner:npg_qUrx9ItSbHa5@ep-weathered-leaf-a67ch667-pooler.us-west-2.aws.neon.tech/usa_nos?sslmode=require"


def fix_names():
    engine = create_engine(DB_URL)
    # 1️⃣ Vérifier colonne father_full_name
    with engine.begin() as conn:
        conn.execute(text("""
            ALTER TABLE persons ADD COLUMN IF NOT EXISTS father_full_name TEXT
        """))

    # 2️⃣ Calculer full_name des pères eux-mêmes
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE persons
            SET full_name = first_name || ' ' || last_name
            WHERE full_name IS NULL
        """))

    # 3️⃣ Calculer father_full_name pour chaque enfant
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE persons p
            SET father_full_name = f.full_name
            FROM persons f
            WHERE p.father_id = f.id
        """))

    with engine.begin() as conn:
        print("🔄 Calcul full_name pères directs")
        conn.execute(text("""
            UPDATE persons
            SET full_name = first_name || ' ' || last_name
            WHERE full_name IS NULL
        """))

    with engine.begin() as conn:
        print("🔄 Calcul full_name enfants")
        updated = True
        while updated:
            result = conn.execute(text("""
                UPDATE persons p
                SET full_name = p.first_name || ' بْنُ ' || f.first_name
                FROM persons f
                WHERE p.father_id = f.id
                  AND p.full_name IS NULL
                  AND f.full_name IS NOT NULL
                RETURNING p.id
            """))
            updated = result.rowcount > 0

    print("✅ Tous les noms calculés !")

if __name__ == "__main__":
    fix_names()
