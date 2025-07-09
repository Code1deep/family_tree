# app/config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(os.path.dirname(basedir), 'instance')

class Config:
    SECRET_KEY = 'dev'  # ou os.environ.get("SECRET_KEY")
    WTF_CSRF_ENABLED = False  # désactive CSRF pour les tests

    # ✅ FORCING: pas de fallback silencieux
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("❌ DATABASE_URL est manquant ! Vérifie ton Render envVars !")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Active les logs SQL pour le débogage

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    # OK pour testing local → SQLite autorisé ici
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(instance_path, 'family.db')}"
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
        "level": "INFO",
        "handlers": ["wsgi"]
    }
}
