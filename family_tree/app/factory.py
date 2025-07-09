# C:\family_tree\app\factory.py
from family_tree.app.extensions import db, babel, login_manager
from sqlalchemy import text
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
                f"{os.getenv('DB_USER', 'hassaniyine_o9yq_user')}:"
                f"{os.getenv('DB_PASSWORD', 'ukL2XI6fd6i7eQpO0uZ39VteUsb1dQ3s')}@"
                f"{os.getenv('DB_HOST', 'dpg-d1m3j4ali9vc73coor00-a')}:"
                f"{os.getenv('DB_PORT', '5432')}/"
                f"{os.getenv('DB_NAME', 'hassaniyine_o9yq')}"
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


            # Test DB
        with app.app_context():
            # Appel anticipé et sûr à full_initialize
            from family_tree.create_persons import create_persons_table
            from family_tree.insertion import full_initialize
            from family_tree.fix_names import fix_names
        
            # Vérifie et crée explicitement
            create_persons_table()
        
            # Vérifie si la table est vide
            rows = db.session.execute(text("SELECT COUNT(*) FROM persons;")).scalar()
            print(f"🔍 Nombre de lignes dans 'persons': {rows}")
        
            if rows == 0:
                print("✅ Table vide → Peuplement...")
                full_initialize()
                fix_names()
                print("✅ Données insérées avec succès.")
            else:
                print("✅ Table 'persons' déjà peuplée.")

            # Test connexion PostgreSQL + création tables
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(text("SELECT 1"))
                    print(f"✓ Test PostgreSQL réussi - Résultat: {result.scalar()}")

                # Inspection tables existantes
                inspector = db.inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"Tables in DB: {tables}")

                print("✓ Connexion PostgreSQL ÉTABLIE et fermée proprement")

            except Exception as e:
                print(f"❌ Erreur de connexion PostgreSQL: {str(e)}")
                raise

            # Vérification templates
            try:
                template_files = os.listdir(app.template_folder)
                print(f"Templates disponibles: {template_files}")
                if 'tree.html' not in template_files:
                    print("❌ Fichier tree.html manquant dans templates")
                else:
                    print("✓ Template tree.html trouvé")
            except Exception as e:
                print(f"❌ Erreur accès templates: {str(e)}")
            
            # Initialisation des services
            try:
                from family_tree.domain.services.person_service import PersonService
                from family_tree.infrastructure.persistence.repositories.person_repo import PersonRepository
                from family_tree.interfaces.api.resources.person.init_person_service import init_person_resources, create_person_api

                from family_tree.interfaces.api.resources.tree.init_tree_service import init_tree_resources

                repo = PersonRepository(db.session)
                person_service = PersonService(repo)
                
                init_person_resources(db.session)
                init_tree_resources(app, person_service)
                print("✓ init_tree_resources exécuté")
                print("✓ Services initialisés")

            except Exception as e:
                print(f"❌ Erreur initialisation services: {str(e)}")
                raise

            # Enregistrement des blueprints
            try:
                from family_tree.interfaces.api.resources.debug.routes_debug import debug_bp
                app.register_blueprint(debug_bp)
                app.register_blueprint(create_person_api(), url_prefix='/api/person')

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

        # Route générique pour tous les fichiers statiques
        @app.route('/static/js/tree/<filename>')
        def serve_tree_js(filename):
            return send_from_directory(os.path.join(BASE_DIR, 'static', 'js', 'tree'), filename)

        # Route spécifique pour les JS (double sécurité)
        @app.route('/js/tree/<filename>')
        def serve_js(filename):
            js_dir = Path(__file__).parent.parent / 'static' / 'js' / 'tree'
            return send_from_directory(js_dir, filename)
        
        print("✅ create_app terminé !")

        return app

    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE dans create_app(): {str(e)}")
        print("Traceback complet:")
        import traceback
        traceback.print_exc()
        raise
