from infrastructure.persistence.db import Base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///family.db")
Base.metadata.create_all(engine)
print("Base de données créée avec succès.")
