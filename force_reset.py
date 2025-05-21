from setup_path import setup_sys_path
setup_sys_path(__file__)

import os
import shutil
from app import create_app
from app.extensions import db

def reset_all():
    # Supprime complètement l'instance
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    if os.path.exists(instance_path):
        shutil.rmtree(instance_path)
    
    # Recrée tout
    app = create_app()
    with app.app_context():
        db.create_all()
    print("Base de données COMPLÈTEMENT réinitialisée")

if __name__ == '__main__':
    reset_all()