import datetime

import pytest

from backend.models import User, Expense, Couple


class TestUser:
    def test_user_create(self):
        user = User(name='John Doe', email='john@example.com', password='password').create()
        assert user.id is not None
        assert user.id is not None
        assert user.password is not None
        assert user.name == 'John Doe'
        assert user.email == 'john@example.com'

    def test_user_belongs_to_couple(self, user1, user2):
        couple = Couple().create()

        user1.join_couple(couple_id=couple.id)
        user2.join_couple(couple_id=couple.id)

        assert user1.couple.id == couple.id
        assert user2.couple_id == couple.id
