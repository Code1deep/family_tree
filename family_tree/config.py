# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(os.path.dirname(basedir), 'instance')

class Config:
    SECRET_KEY = 'dev'  # ou os.environ.get("SECRET_KEY")
    WTF_CSRF_ENABLED = False  # désactive CSRF pour les tests
    
    """Configuration de base commune à tous les environnements."""
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    "postgresql://postgres:123@localhost:5432/family"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Active les logs SQL pour le débogage

class DevelopmentConfig(Config):
    """Configuration spécifique au développement."""
    DEBUG = True

class TestingConfig(Config):
    """Configuration utilisée pour les tests unitaires."""
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    "postgresql://postgres:123@localhost:5432/family"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "root": {
        "level": "INFO",  # Peut être DEBUG pour plus de détails
        "handlers": ["wsgi"]
    }
}
