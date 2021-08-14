import json

import requests
from flask import request
from source import google_client
from source.models import User


class GoogleAuthManager:
    def __init__(self, discovery_url, client_id, client_secret) -> None:
        self.google_provider_cfg = GoogleAuthManager.get_google_provider_cfg(discovery_url)
        self.token_endpoint = self.google_provider_cfg["token_endpoint"]
        self.userinfo_endpoint = self.google_provider_cfg["userinfo_endpoint"]
        self.client_id = client_id
        self.client_secret = client_secret

    @staticmethod
    def get_google_provider_cfg(discovery_url):
        return requests.get(discovery_url).json()

    @classmethod
    def get_request_uri(cls, discovery_url):
        google_provider_cfg = cls.get_google_provider_cfg(discovery_url)
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = google_client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return request_uri

    def get_token(self, code):
        token_url, headers, body = google_client.prepare_token_request(
            self.token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(
                self.client_id,
                self.client_secret,
            ),
        )
        return token_response.json()

    def get_user(self, token):
        google_client.parse_request_body_response(json.dumps(token))
        uri, headers, body = google_client.add_token(self.userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            return "User email not available or not verified by Google.", 400
        user = User(id=unique_id, name=users_name, email=users_email, profile_pic=picture)
        if not User.get_user_with_id(user.id):
            user.create_user()
        return user
