import datetime
import json

import pytest

from backend.models import Couple, Expense
class TestUserApis:
    def test_current_user(self, user1, client, mock_decode_token):
        response = client.get('/api/user/current',
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': f'Bearer TOKEN'
                              }
                              )
        assert response.json['user']['id'] == user1.id

    def test_user_balance_based_on_expenses(self, client, user1, user2, mock_decode_token):
        couple = Couple().create()
        user1.join_couple(couple_id=couple.id)
        user2.join_couple(couple_id=couple.id)
        Expense(
            total=40.0,
            title='Expense 1',
            couple_id=couple.id,
            created_at=datetime.datetime(2023, 5, 17),
            paid_by_user_id=user1.id
        ).create()


        response = client.get('/api/user/balance',
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': f'Bearer TOKEN'
                              }
                              )
        assert response.json['balance'] == 20