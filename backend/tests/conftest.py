import pytest
from flask import Flask
from sqlalchemy.orm import sessionmaker

from backend.app import create_app, db as _db
from backend.models import User


class TestConfig(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'test'
    TESTING = True


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app(config_name='testing')

    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.yield_fixture(scope='session')
def db(app):
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    yield db.session()

    transaction.rollback()
    connection.close()
    db.session.remove()

@pytest.fixture
def user1():
    return User(name='John Doe', email='john@example.com', password='password').create()

@pytest.fixture
def user2():
    return User(name='Jane Doe', email='jane@example.com', password='password').create()


