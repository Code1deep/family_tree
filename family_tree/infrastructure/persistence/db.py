# infrastructure/persistence/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# On récupère l'URL de connexion à PostgreSQL depuis les variables d'environnement
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL n'est pas défini dans l'environnement !")

print(f"DATABASE_URL utilisé : {DATABASE_URL}")

# Création de l'engine PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

# Session locale avec scoped_session
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

# Base pour les modèles
Base = declarative_base()

# db_session utilisable dans ton app
db_session = SessionLocal()

# Optionnel : fonction pour initialiser une base en mémoire pour des tests (non utilisé en prod)
def init_db_for_tests():
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSession = sessionmaker(bind=test_engine)
    Base.metadata.create_all(test_engine)
    return test_engine, TestingSession

__all__ = ["engine", "SessionLocal", "db_session", "Base"]
