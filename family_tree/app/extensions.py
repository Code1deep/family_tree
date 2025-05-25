# \app\extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_migrate import Migrate
from huggingface_hub import User

db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()
migrate = Migrate()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
