# C:\family_tree\app\factory.py
from family_tree.app.extensions import db, babel, login_manager

# Ensuite seulement les autres imports
from family_tree.infrastructure.persistence.db import db_session
import os
from pathlib import Path
from flask_wtf.csrf import CSRFProtect
from flask import Flask, request, current_app, send_from_directory, url_for
import logging.config
from family_tree.app.config import LOGGING_CONFIG
import psycopg2  

from family_tree.interfaces.auth import auth_bp, load_user
print("✓ Import auth_bp & load_user OK")


# Configuration des chemins
BASE_DIR = Path(__file__).resolve().parent.parent 
#sys.path.insert(0, str(BASE_DIR))

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
#for p in sys.path:
 #  print(p)
#print("====================\n")

_app_creation_count = 0

import os
for root, dirs, files in os.walk(str(BASE_DIR / 'static')):
    for file in files:
        print(f"STATIC FILE FOUND: {os.path.join(root, file)}")


def create_app(config_object='config.Config', testing=False):
    """Factory d'application Flask avec configuration PostgreSQL"""
    global _app_creation_count
    _app_creation_count += 1
    print(f"create_app() appelé {_app_creation_count} fois")

    try:
        # Initialisation de l'app avec chemins absolus
        app = Flask(__name__,
                   instance_relative_config=True,
                   template_folder=os.path.join(BASE_DIR, 'app', 'templates'),
                   static_url_path='/static',
                   static_folder=os.path.join(BASE_DIR, 'static'))
        
        # Debug des chemins
        print(f"\n=== CONFIGURATION PATHS ===")
        print(f"Instance path: {app.instance_path}")
        print(f"Template path: {app.template_folder}")
        print(f"Static path: {app.static_folder}")
        if app.static_folder is not None:
            print(f"Static folder path Flask: {app.static_folder}")
            print(f"Static folder exists: {os.path.exists(app.static_folder)}")
        else:
            print("⚠ app.static_folder is None")

        # Debug complet des chemins
        print(f"\n=== DEBUG BASE_DIR ===")
        print(f"__file__: {__file__}")
        print(f"Path(__file__).resolve(): {Path(__file__).resolve()}")
        print(f"BASE_DIR: {BASE_DIR}")
        print(f"BASE_DIR parent: {BASE_DIR.parent}")
        print(f"BASE_DIR grand-parent: {BASE_DIR.parent.parent}")

        # Simule ce que Flask reçoit
        static_test_path = os.path.join(BASE_DIR, 'static')
        print(f"STATIC PATH CALCULÉ: {static_test_path}")
        print(f"Ce dossier existe-t-il ? {os.path.exists(static_test_path)}")

        # Configuration
        app.config.from_object(config_object)
        app.secret_key = 'super secret string'  # 🔐 sécurise ensuite
        db_path = os.path.join(app.instance_path, 'family.db')

        print(f"DB path: {db_path}")
        app.config.update(
            SQLALCHEMY_DATABASE_URI=(
                f"postgresql+psycopg2://"
                f"{os.getenv('DB_USER', 'hassaniyine_user')}:"
                f"{os.getenv('DB_PASSWORD', 'MTzpda6BklFr8W0rLUIn1ohgFaN1xfLL')}@"
                f"{os.getenv('DB_HOST', 'dpg-d1biad6uk2gs739qeh10-a')}:"
                f"{os.getenv('DB_PORT', '5432')}/"
                f"{os.getenv('DB_NAME', 'hassaniyine')}"
            ),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SQLALCHEMY_ENGINE_OPTIONS={
                'pool_size': 10,
                'max_overflow': 20,
                'pool_pre_ping': True,
                'pool_recycle': 3600
            }
        )

        print(f"PostgreSQL URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

        # Vérification des dossiers
        os.makedirs(app.instance_path, exist_ok=True)
        print(f"Instance folder exists: {os.path.exists(app.instance_path)}")
        print(f"Template folder exists: {os.path.exists(app.template_folder) if app.template_folder else 'N/A'}")
        print(f"Static folder exists: {os.path.exists(app.static_folder) if app.static_folder else 'N/A'}")

        # Initialisation des extensions
        csrf = CSRFProtect()
        csrf.init_app(app)
        db.init_app(app)
        babel.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'

            # User loader
        login_manager.user_loader(load_user)

        # Enregistrement des blueprints
        app.register_blueprint(auth_bp)

        # Middleware logging
        @app.before_request
        def log_request_info():
            current_app.logger.info(f"[ROUTE] {request.method} {request.path}")
    
            if request.is_json:
                current_app.logger.info(f"[BODY] {request.get_json()}")
    
            if request.args:
                current_app.logger.info(f"[ARGS] {request.args}")
    
            if request.form:
                current_app.logger.info(f"[FORM] {request.form}")

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            """Ferme proprement les sessions SQLAlchemy"""
            db.session.remove()

        # Route de base
        @app.route('/')
        def home():
            return "Bienvenue sur Family Tree API", 200

        @app.route('/static/js/tree/<path:filename>')
        def serve_js_tree(filename):
            return send_from_directory(os.path.join(BASE_DIR, 'static', 'js', 'tree'), filename)

        with app.test_request_context():
            print("✅ STATIC PATH TESTS")
            print(url_for('static', filename='js/tree/core.js'))
            print(url_for('static', filename='js/tree/d3-tree.js'))
            print(url_for('static', filename='images/logo.png'))
        
        with app.app_context():
            # Test de connexion DB avec PostgreSQL
            try:
                # Vérification de la connexion PostgreSQL - Version corrigée
                with db.engine.connect() as conn:
                    # Utilisation de text() pour créer une expression SQL correcte
                    from sqlalchemy import text
                    result = conn.execute(text("SELECT 1"))
                    print(f"✓ Test PostgreSQL réussi - Résultat: {result.scalar()}")

                    # Création des tables si elles n'existent pas
                    db.create_all()

                    # Inspection des tables
                    inspector = db.inspect(db.engine)
                    print(f"Tables in DB: {inspector.get_table_names()}")

                print("✓ Connexion PostgreSQL ÉTABLIE et fermée proprement")
            except Exception as e:
                print(f"❌ Erreur de connexion PostgreSQL: {str(e)}")
                raise

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
            
            from family_tree.insertion import full_initialize
            full_initialize()
            
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
