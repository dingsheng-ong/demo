import os
import pytest

@pytest.fixture
def app():
    from demo import create_app
    app = create_app()
    yield app

@pytest.fixture(scope='function')
def db():
    from demo import db
    db.drop_all()
    yield db
    db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def env(monkeypatch):
    # make a copy of all env. variables
    env = os.environ.copy()
    yield
    # restore environment variables
    for k, v in env.items():
        monkeypatch.setenv(k, v)
