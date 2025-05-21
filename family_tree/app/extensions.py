# \app\extensions.py
from setup_path import setup_sys_path
setup_sys_path(__file__)

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()
migrate = Migrate()