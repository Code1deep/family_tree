# infrastructure/persistence/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# On récupère l'URL de connexion à PostgreSQL depuis les variables d'environnement
# Essaie de récupérer DATABASE_URL directement
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("🌐 DATABASE_URL absent, construction dynamique...")
    DB_USER = os.getenv('DB_USER', 'hassaniyine_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'MTzpda6BklFr8W0rLUIn1ohgFaN1xfLL')
    DB_HOST = os.getenv('DB_HOST', 'db')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'hassaniyine')
    
    DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    print(f"✅ DATABASE_URL construit : {DATABASE_URL}")

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
