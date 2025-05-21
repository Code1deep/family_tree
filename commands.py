# C:\family_tree\commands.py

from setup_path import setup_sys_path
setup_sys_path(__file__)

import click
from flask.cli import with_appcontext
from app.extensions import db
from domain.models.person import Person

def register_commands(app):
    """Enregistre les commandes CLI avec l'application Flask"""
    
    @app.cli.command("populate_ali_family")
    @with_appcontext
    def populate_ali_family():
        """Peuple la base de données avec la famille d'Ali"""
        try:
            db.drop_all()
            db.create_all()

            abu_talib = Person(id=2, first_name="Abu", last_name="Talib", gender="male")
            fatima_bint_asad = Person(id=3, first_name="Fatima", last_name="bint Asad", gender="female")

            ali = Person(
                id=1, 
                first_name="Ali", 
                last_name="Ibn Abi Talib",
                gender="male",
                father_id=2,
                mother_id=3
            )

            hassan = Person(
                id=4, 
                first_name="Hassan", 
                last_name="Ibn Ali",
                gender="male",
                father_id=1,
                mother_id=3
            )

            hussein = Person(
                id=5, 
                first_name="Hussein", 
                last_name="Ibn Ali",
                gender="male",
                father_id=1,
                mother_id=3
            )

            db.session.add_all([abu_talib, fatima_bint_asad, ali, hassan, hussein])
            db.session.commit()
            print("✅ Famille d'Ali insérée avec succès.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur: {str(e)}")
            raise e