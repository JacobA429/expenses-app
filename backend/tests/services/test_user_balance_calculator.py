import datetime

import pytest

from backend.models import Expense, Couple
from backend.services import UserBalanceCalculator


@pytest.mark.user_balance_calculator
class TestUserBalanceCalculator:
    def test_balance_for_user_returns_negative_balance_if_user_owes_money(self,user1, user2):
        couple = Couple().create()
        user1.join_couple(couple.id)
        user2.join_couple(couple.id)

        expenses = [
            Expense(
                total=50.0,
                title='Expense 1',
                couple_id=couple.id,
                created_at=datetime.datetime(2023, 5, 17),
                paid_by_user_id=user1.id
            ).create(),
            Expense(
                total=100.0,
                title='Expense 1',
                couple_id=couple.id,
                created_at=datetime.datetime(2023, 5, 17),
                paid_by_user_id=user2.id
            ).create()
        ]

        balance = UserBalanceCalculator.balance_for_user(user1, expenses )
        assert balance == -25.0

    def test_balance_for_user_returns_positive_balance_if_user_is_owed_money(self,user1, user2):
        couple = Couple().create()
        user1.join_couple(couple.id)
        user2.join_couple(couple.id)

        expenses = [
            Expense(
                total=100.0,
                title='Expense 1',
                couple_id=couple.id,
                created_at=datetime.datetime(2023, 5, 17),
                paid_by_user_id=user1.id
            ).create(),
            Expense(
                total=20.0,
                title='Expense 1',
                couple_id=couple.id,
                created_at=datetime.datetime(2023, 5, 17),
                paid_by_user_id=user2.id
            ).create()
        ]

        balance = UserBalanceCalculator.balance_for_user(user1, expenses )
        assert balance == 40.0
