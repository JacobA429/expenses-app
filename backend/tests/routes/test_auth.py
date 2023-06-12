import json

import pytest

from backend.models import User


@pytest.mark.signup
class TestSignUp:
    def test_signup_returns_201(self, client):
        response = client.post('/auth/signup', data=json.dumps({
            'email': 'user@email',
            'password': 'password',
            'name': 'user'
        }), headers={'Content-Type': 'application/json'})

        assert response.status_code == 201

    def test_signup_creates_a_new_user(self, client):
        client.post('/auth/signup', data=json.dumps({
            'email': 'user@email',
            'password': 'password',
            'name': 'user'
        }), headers={'Content-Type': 'application/json'})

        new_user = User.query.filter_by(email='user@email').first()
        assert new_user is not None
        assert new_user.name == 'user'

    def test_signup_returns_409_for_existing_user(self, client):
        User(name='user', email='user@email', password='password').create()

        response = client.post('/auth/signup', data=json.dumps({
            'email': 'user@email',
            'password': 'password',
            'name': 'John Doe'
        }), headers={'Content-Type': 'application/json'})

        assert response.status_code == 409


@pytest.mark.login
class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        User(name='John Doe', email='john@example.com', password='password').create()

    def test_login_returns_authenticated_token(self, client):
        response = client.post('/auth/login', data=json.dumps({
            'email': 'john@example.com',
            'password': 'password',
        }), headers={'Content-Type': 'application/json'})

        assert response.json['token'] is not None

    def test_login_returns_401_if_email_is_missing(self, client):
        response = client.post('/auth/login', data=json.dumps({
            'email': '',
            'password': 'password',
        }), headers={'Content-Type': 'application/json'})

        assert response.status_code == 401

    def test_login_returns_401_if_password_is_missing(self, client):
        response = client.post('/auth/login', data=json.dumps({
            'password': '',
            'email': 'john@example.com',
        }), headers={'Content-Type': 'application/json'})

        assert response.status_code == 401

    def test_login_returns_401_if_email_does_not_match_a_user(self, client):
        response = client.post('/auth/login', data=json.dumps({
            'password': 'password',
            'email': 'user@example.com',
        }), headers={'Content-Type': 'application/json'})

        assert response.status_code == 401
        assert response.json['message'] == 'No user with email found'
    def test_login_returns_401_if_password_does_not_match(self, client):
        response = client.post('/auth/login', data=json.dumps({
            'password': 'wrong_password',
            'email': 'john@example.com',
        }), headers={'Content-Type': 'application/json'})

        assert response.status_code == 401
        assert response.json['message'] == 'Could not verify email and password'
