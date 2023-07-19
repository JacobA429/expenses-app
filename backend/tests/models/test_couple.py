import datetime

import pytest

from backend.models import User, Expense, Couple
class TestCouple:

    def test_couple_has_many_expenses(self, user1, user2):
        couple = Couple().create()

        Expense(
            total=40.0,
            title='Expense 1',
            couple_id=couple.id,
            created_at=datetime.datetime(2023, 5, 17),
            paid_by_user_id=user1.id
        ).create()

        Expense(
            total=10.0,
            title='Expense 2',
            couple_id=couple.id,
            created_at=datetime.datetime(2023, 1, 1),
            paid_by_user_id=user2.id
        ).create()

        assert couple.expenses.count() == 2