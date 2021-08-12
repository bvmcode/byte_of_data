import requests
import json
from flask import Blueprint, render_template, current_app, request, redirect, url_for
from oauthlib.oauth2 import WebApplicationClient
from source.models import User
from flask_login import login_user, logout_user, current_user, login_required

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
    print(request_uri)
    return redirect(request_uri)


@users_blueprint.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    print('hello')
    client = WebApplicationClient(current_app.config["GOOGLE_CLIENT_ID"])
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    print(google_provider_cfg)
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config["GOOGLE_CLIENT_ID"], current_app.config["GOOGLE_CLIENT_SECRET"]),
    )

    # Parse the tokens!
    
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id=unique_id, name=users_name, email=users_email, profile_pic=picture
    )
    
    # Doesn't exist? Add it to the database.
    if not User.get_user_with_id(unique_id):
        user.create_user()

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("users.index"))

@users_blueprint.route("/index")
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login_page">Google Login</a>'

@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.index"))
