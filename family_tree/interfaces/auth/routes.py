# interfaces/auth/routes.py
import flask
from flask import Blueprint
import flask_login
from family_tree.interfaces.auth.user import users, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return '''<form action="/auth/login" method="POST">
                    <input type='text' name='email'>
                    <input type='password' name='password'>
                    <input type='submit'>
                  </form>'''
    email = flask.request.form["email"]
    if email in users and flask.request.form["password"] == users[email]["password"]:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for("protected"))
    return "Bad login", 401

@auth_bp.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"
