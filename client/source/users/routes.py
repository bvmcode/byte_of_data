import requests
from flask import Blueprint, render_template, current_app, request, redirect
from oauthlib.oauth2 import WebApplicationClient

users_blueprint = Blueprint("users", __name__)


def get_google_provider_cfg():
    return requests.get(current_app.config["GOOGLE_DISCOVERY_URL"]).json()


@users_blueprint.route("/login_page")
def login_page():
    return render_template("users/login.html")


@users_blueprint.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    client = WebApplicationClient(current_app.config["GOOGLE_CLIENT_ID"])
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)
