# # backend/tests/test_models.py
# import unittest
from backend.models import User


def test_user_create():
    user = User(name='John Doe', email='john@example.com', password='password').create()
    assert user.id is not None
    assert user.id is not None
    assert user.password is not None
    assert user.name == 'John Doe'
    assert user.email == 'john@example.com'
