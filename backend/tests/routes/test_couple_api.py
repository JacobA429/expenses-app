import datetime
import json

import pytest

from backend.models import Couple, Expense
class TestCoupleApi:
    def test_couple(self, user1, user2, client, mock_decode_token):
        couple = Couple().create()
        user1.join_couple(couple_id=couple.id)
        user2.join_couple(couple_id=couple.id)

        response = client.get('/api/couple/current',
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': f'Bearer TOKEN'
                              }
                              )
        assert response.json['couple']['id'] == couple.id

    def test_create_couple(self, client, user1, user2):
        response = client.post('/api/couple/create',
                               data=json.dumps({
                                   'user1_id': user1.id,
                                   'user2_id': user2.id
                               }),
                               headers={
                                   'Content-Type': 'application/json',
                               }
                               )

        couple_id = response.json['id']
        couple = Couple.query.filter_by(id=couple_id).first()
        assert couple_id is not None
        assert couple is not None
        assert couple.users is not None


    def test_returns_all_expenses_for_couple(self, client, user1, user2, mock_decode_token):
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

        Expense(
            total=10.0,
            title='Expense 2',
            couple_id=couple.id,
            created_at=datetime.datetime(2023, 1, 1),
            paid_by_user_id=user2.id
        ).create()

        response = client.get('/api/couple/current',
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': f'Bearer TOKEN'
                              }
                              )

        assert response.status_code == 200
        assert len(response.json['couple']['expenses']) == 2
