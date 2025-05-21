from setup_path import setup_sys_path
setup_sys_path(__file__)

#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

from domain.models.person import Person  # si tu as une classe Person dans person.py

__all__ = ["Person"]


