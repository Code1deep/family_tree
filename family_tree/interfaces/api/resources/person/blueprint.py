# interfaces/api/resources/person/blueprint.py
# Déclare seulement le blueprint, sans routes ni import de services
from flask import Blueprint

person_api = Blueprint("person_api", __name__)
