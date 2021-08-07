from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name="DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(f"source.config.{config_name}")

    db.init_app(app)
    login_manager.init_app(app)

    from source.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user_with_id(user_id)

    from source.main.routes import main_blueprint
    from source.users.routes import users_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(users_blueprint)

    return app
