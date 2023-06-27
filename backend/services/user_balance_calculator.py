import datetime
from typing import List

import jwt

from backend.models import Expense


class UserBalanceCalculator:

    @classmethod
    def balance_for_user(cls, user, expenses: List[Expense]):
        balance = 0
        if expenses.count() == 0:
            return balance

        for expense in expenses:
            split_total = expense.total / 2
            if expense.paid_by_user_id == user.id:
                balance += split_total
            else:
                balance -= split_total
        return balance
