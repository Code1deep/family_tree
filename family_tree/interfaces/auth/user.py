# interfaces/auth/user.py
from flask_login import UserMixin
from app.extensions import login_manager

# Simuler un utilisateur
users = {'foo@bar.com': {'password': 'secret'}}

class User(UserMixin):
    def __init__(self, user_id=None):
        self.id = user_id  # <-- ici on définit l'attribut proprement

@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return None
    return User(user_id)
