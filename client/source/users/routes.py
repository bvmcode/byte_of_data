from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from source.models import User
from source.users.utils import GoogleAuthManager

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/login")
def login():
    request_uri = GoogleAuthManager.get_request_uri(current_app.config["GOOGLE_DISCOVERY_URL"])
    return redirect(request_uri)


@users_blueprint.route("/login/callback")
def callback():
    code = request.args.get("code")
    google = GoogleAuthManager(
        current_app.config["GOOGLE_DISCOVERY_URL"],
        current_app.config["GOOGLE_CLIENT_ID"],
        current_app.config["GOOGLE_CLIENT_SECRET"],
    )
    token = google.get_token(code)
    user = google.get_user(token)
    login_user(user)
    return redirect(url_for("main.home"))


@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))
