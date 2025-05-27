# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(os.path.dirname(basedir), 'instance')

class Config:
    SECRET_KEY = 'dev'  # ou os.environ.get("SECRET_KEY")
    WTF_CSRF_ENABLED = False  # désactive CSRF pour les tests
    
    """Configuration de base commune à tous les environnements."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(instance_path, 'family.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # Active les logs SQL pour le débogage

class DevelopmentConfig(Config):
    """Configuration spécifique au développement."""
    DEBUG = True

class TestingConfig(Config):
    """Configuration utilisée pour les tests unitaires."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(instance_path, 'family.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
