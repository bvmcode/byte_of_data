import pytest
from source import create_app


@pytest.fixture(scope="module")
def test_app():
    app = create_app("TestingConfig")
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def client(test_app):
    yield test_app.test_client()
