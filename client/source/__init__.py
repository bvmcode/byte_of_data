from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from celery import Celery
from source.config import BaseConfig

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
print(__name__, flush=True)
celery = Celery(__name__, broker=BaseConfig.CELERY_BROKER_URL, backend=BaseConfig.CELERY_RESULT_BACKEND)

def create_app(config_name="DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(f"source.config.{config_name}")

    db.init_app(app)
    login_manager.init_app(app)
    
    from source.main.routes import main_blueprint
    from source.users.routes import users_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(users_blueprint)

    return app
