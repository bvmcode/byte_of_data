import os


class BaseConfig:
    BASE_DIR = os.path.join(os.path.abspath(os.path.curdir), os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")

class DevelopmentConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(BaseConfig):
    SECRET_KEY = "123"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
