# C:\family_tree\app\factory.py 
from setup_path import setup_sys_path
setup_sys_path(__file__)

from flask import Flask, app
from app.extensions import db, babel, login_manager
from infrastructure.persistence.db import db_session
from interfaces.api.resources.tree_resource import create_tree_api
import os

_app_creation_count = 0 

def create_app(config_object='config.Config', testing=False):
    """Factory d'application Flask"""
    global _app_creation_count
    _app_creation_count += 1
    print(f"create_app() appelé {_app_creation_count} fois")

    app = Flask(__name__)
    if testing:
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object(config_object)


    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'family.db')
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialisation des extensions
    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    with app.app_context():
        # Création des tables
        from domain.models.person import Person
        db.create_all()

        # Initialisation du service
        from domain.services.person_service import PersonService
        from infrastructure.persistence.repositories.person_repo import PersonRepository
        repo = PersonRepository(db.session)
        person_service = PersonService(repo)

        # Initialisation des ressources Person
        from interfaces.api.resources.person_resource import create_person_api, init_resources
    
        person_api = create_person_api(person_service)

        # Enregistrement des blueprints
        print("Blueprints enregistrés avant:", list(app.blueprints.keys()))
        if 'person_api' not in app.blueprints:
            app.register_blueprint(person_api)
            print("Blueprints enregistrés après:", list(app.blueprints.keys()))

        # Arbre
        from interfaces.api.resources.tree_resource import create_tree_api
        app.register_blueprint(create_tree_api(person_service), url_prefix="/api")

        # Enregistrement des commandes CLI
        from commands import register_commands
        register_commands(app)

        # Enregistrer le blueprint pour les erreurs
        from app.errors import errors
        app.register_blueprint(errors)
        # Test de connexion
        try:
            db.engine.connect()
            print("✓ Connexion DB ÉTABLIE")
        except Exception as e:
            print(f"Erreur connexion DB : {e}")

    return app
