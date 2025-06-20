# interfaces/api/resources/home/routes_home.py
from flask import Blueprint, render_template

def register_home_routes(app):
    home_bp = Blueprint("home", __name__)

    @home_bp.route('/')
    def home():
        # Remplace ces valeurs par des vraies stats de ta DB
        return render_template("home.html",
                               total_persons=100,
                               alive_persons=80,
                               male_persons=50,
                               female_persons=50,
                               recent_persons=[])

    app.register_blueprint(home_bp)
