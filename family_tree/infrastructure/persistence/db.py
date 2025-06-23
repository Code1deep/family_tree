# infrastructure/persistence/db.py


import os
from family_tree.app.extensions import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# Exemple de configuration de la base 
# Définit un chemin absolu vers family.db dans le dossier instance
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'instance'))
DATABASE_PATH = os.path.join(BASE_DIR, "family.db")

DATABASE_URL = os.getenv('DATABASE_URL')


print("DB PATH:", os.path.abspath("family.db"))

print("DATABASE_URL:", DATABASE_URL)


engine = create_engine(DATABASE_URL, echo=True)

# Session locale avec scoped_session
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

# Base pour les modèles
Base = declarative_base()

# db_session est maintenant accessible
db_session = SessionLocal()

# Permet d'utiliser une base en mémoire pour les tests
def init_db_for_tests():
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSession = sessionmaker(bind=test_engine)
    Base.metadata.create_all(test_engine)
    return test_engine, TestingSession

#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy()

__all__ = ["engine", "SessionLocal", "db_session", "Base"]
