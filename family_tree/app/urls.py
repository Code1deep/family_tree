# C:\family_tree\app\urls.py
from flask import Blueprint, send_from_directory
from family_tree.app.factory import create_app
import os

# Création d'un blueprint pour les routes principales
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return "Bienvenue sur Family Tree"

# Routes pour les fichiers statiques (complémentaires à celles de factory.py)
@main_bp.route('/static/<path:filename>')
def serve_static(filename):
    static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')
    return send_from_directory(static_folder, filename)

# Configuration spécifique des routes JS
@main_bp.route('/js/tree/<path:filename>')
def serve_js_tree(filename):
    return send_from_directory('../static/js/tree', filename)

# Configuration des routes d'API
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/version')
def api_version():
    return {'version': '1.0.0'}

def configure_routes(app):
    """Configure toutes les routes de l'application"""
    # Enregistrement des blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    # Routes complémentaires (exemple)
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    # Debug des routes enregistrées
    print("\n=== ROUTES CONFIGURÉES ===")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")
