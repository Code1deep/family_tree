# C:\family_tree\app\factory.py

from family_tree.app.extensions import db, babel, login_manager
from family_tree.infrastructure.persistence.db import db_session
import os
import sys
from pathlib import Path
from flask import Flask, request  
from flask_wtf.csrf import CSRFProtect

# Configuration des chemins
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

# Debug - Affiche la structure
print(f"\n=== STRUCTURE DU PROJET ===")
for root, dirs, files in os.walk(BASE_DIR):
    level = root.replace(str(BASE_DIR), '').count(os.sep)
    indent = ' ' * 4 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")

print("\n=== CHEMIN PYTHON ===")
for p in sys.path:
    print(p)
print("====================\n")

_app_creation_count = 0

def create_app(config_object='config.Config', testing=False):
    """Factory d'application Flask avec debug complet"""
    global _app_creation_count
    _app_creation_count += 1
    print(f"create_app() appelé {_app_creation_count} fois")

    try:
        # Initialisation de l'app avec chemins absolus
        app = Flask(__name__,
                   instance_relative_config=True,
                   template_folder=os.path.join(BASE_DIR, 'app/templates'),
                   static_folder=os.path.join(BASE_DIR, 'static'))  # Modifié pour correspondre à votre structure
        
        # Debug des chemins
        print(f"\n=== CONFIGURATION PATHS ===")
        print(f"Instance path: {app.instance_path}")
        print(f"Template path: {app.template_folder}")
        print(f"Static path: {app.static_folder}")

        # Configuration
        app.config.from_object(config_object)
        db_path = os.path.join(app.instance_path, 'family.db')
        app.config.update(
            SQLALCHEMY_DATABASE_URI=f'sqlite:///{db_path}',
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
        print(f"DB path: {db_path}")

        # Vérification des dossiers
        os.makedirs(app.instance_path, exist_ok=True)
        print(f"Instance folder exists: {os.path.exists(app.instance_path)}")
        print(f"Template folder exists: {os.path.exists(app.template_folder)}")
        print(f"Static folder exists: {os.path.exists(app.static_folder)}")

        # Initialisation des extensions
        csrf = CSRFProtect()
        csrf.init_app(app)
        db.init_app(app)
        babel.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'

        # Route de base
        @app.route('/')
        def home():
            return "Bienvenue sur Family Tree API", 200

        with app.app_context():
            # Test de connexion DB
            try:
                db.create_all()
                # Méthode moderne pour lister les tables
                inspector = db.inspect(db.engine)
                print(f"Tables in DB: {inspector.get_table_names()}")
                print("✓ Connexion DB ÉTABLIE")
            except Exception as e:
                print(f"❌ Erreur DB: {str(e)}")

            # Vérification des templates
            try:
                template_files = os.listdir(app.template_folder)
                print(f"Templates disponibles: {template_files}")
                if 'tree.html' not in template_files:
                    print("❌ Fichier tree.html manquant dans templates")
                else:
                    print("✓ Template tree.html trouvé")
            except Exception as e:
                print(f"❌ Erreur accès templates: {str(e)}")
            from family_tree.domain.models.person import Person   
            
            from family_tree.insertion import initialize_data
            initialize_data()
            
            # Initialisation des services
            try:
                from family_tree.domain.services.person_service import PersonService
                from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
                from family_tree.interfaces.api.resources.person import init_person_resources
                from family_tree.interfaces.api.resources.tree import init_tree_resources
                init_person_resources(app)
                init_tree_resources(app, person_service)
                repo = PersonRepository(db.session)
                person_service = PersonService(repo)
                print("✓ Services initialisés")
            except Exception as e:
                print(f"❌ Erreur initialisation services: {str(e)}")
                raise

            # Enregistrement des blueprints
            try:
                from family_tree.interfaces.api.resources.tree.init_tree_service import create_tree_api
                #from family_tree.interfaces.api.resources.person.init_person_service import create_person_api
                from family_tree.interfaces.api.resources.person import person_api

                app.register_blueprint(person_api, url_prefix='/api/persons')
                app.register_blueprint(create_tree_api(person_service), url_prefix='/api/tree')
                
                # Debug des routes enregistrées
                print("✓ Blueprints enregistrés")
                print("Routes disponibles:")
                for rule in app.url_map.iter_rules():
                    print(f" - {rule}")
            except Exception as e:
                print(f"❌ Erreur enregistrement blueprints: {str(e)}")
                raise

        # Middleware de debug pour les requêtes (corrigé)
        @app.after_request
        def log_request(response):
            if request:  # Vérification supplémentaire
                print(f"[REQUEST] {request.method} {request.path} -> {response.status}")
            return response

        return app

    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE dans create_app(): {str(e)}")
        print("Traceback complet:")
        import traceback
        traceback.print_exc()
        raise

