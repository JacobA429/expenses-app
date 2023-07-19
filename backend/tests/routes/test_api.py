import datetime
import json

import pytest

from backend.models import Couple, Expense


@pytest.mark.partner_link
class TestPartnerLink:

    @pytest.fixture
    def mock_decode_token(self, mocker, user1):
        # Mock JwtService.decode_token
        mock_token = mocker.patch('backend.services.JwtService.decode_token')
        mock_token.return_value = user1.id

    @pytest.fixture
    def mock_generate_invite_token(self, mocker):
        # Mock JwtService.decode_token
        mock_token = mocker.patch('backend.services.PartnerInviteService.generate_invite_token')
        mock_token.return_value = "ABCD"

    def test_generate_partner_link(self, client, mock_decode_token, mock_generate_invite_token):
        response = client.get('/api/partner_link',
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': f'Bearer TOKEN'
                              }
                              )

        assert response.json['link'] == 'http://localhost:3000/join/ABCD'

    def test_returns_401_if_decoding_errors(self, client):
        response = client.get('/api/partner_link',
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': f'Bearer TOKEN'
                              }
                              )

        assert response.status_code == 401


@pytest.mark.join
class TestJoin:
    @pytest.fixture
    def mock_decode_invite_token(self, mocker, user1):
        # Mock JwtService.decode_token
        mock_token = mocker.patch('backend.services.PartnerInviteService.decode_invite_token')
        mock_token.return_value = user1.id

    def test_join_returns_original_user(self, client, mock_decode_invite_token):
        response = client.get('/api/join/ABCD',
                              headers={
                                  'Content-Type': 'application/json',
                              }
                              )
        assert response.json['user1']['email'], 'john@example.com'


@pytest.mark.create_couple
class TestCreateCouple:
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


@pytest.mark.expenses
class TestExpenses:
    couple = None

    @pytest.fixture(autouse=True)
    def setup(self, user1, user2):
        self.couple = Couple().create()
        user1.join_couple(couple_id=self.couple.id)
        user2.join_couple(couple_id=self.couple.id)

    @pytest.fixture
    def mock_decode_token(self, mocker, user1):
        # Mock JwtService.decode_token
        mock_token = mocker.patch('backend.services.JwtService.decode_token')
        mock_token.return_value = user1.id

    def test_returns_all_expenses_for_couple(self, client, mock_decode_token, user1, user2):
        Expense(
            total=40.0,
            title='Expense 1',
            couple_id=self.couple.id,
            created_at=datetime.datetime(2023, 5, 17),
            paid_by_user_id=user1.id
        ).create()

        Expense(
            total=10.0,
            title='Expense 2',
            couple_id=self.couple.id,
            created_at=datetime.datetime(2023, 1, 1),
            paid_by_user_id=user2.id
        ).create()

        response = client.get('/api/expenses/all',
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': f'Bearer TOKEN'
                              }
                              )

        assert response.status_code == 200
        assert len(response.json['expenses']) == 2

    def test_expenses_return_empty_array_if_no_expenses(self, client, mock_decode_token):
        response = client.get('/api/expenses/all',
                              headers={
                                  'Content-Type': 'application/json',
                                  'Authorization': f'Bearer TOKEN'
                              }
                              )

        assert response.status_code == 200
        assert len(response.json['expenses']) == 0


@pytest.mark.create_expenses
class TestCreateExpense:
    couple = None

    @pytest.fixture
    def mock_decode_token(self, mocker, user1):
        # Mock JwtService.decode_token
        mock_token = mocker.patch('backend.services.JwtService.decode_token')
        mock_token.return_value = user1.id

    @pytest.fixture(autouse=True)
    def setup(self, user1, user2):
        self.couple = Couple().create()
        user1.join_couple(couple_id=self.couple.id)
        user2.join_couple(couple_id=self.couple.id)

    def test_creates_expense(self, client, mock_decode_token, user1):
        response = client.post('/api/expenses/create', data=json.dumps({
            'title': 'Expense 1',
            'total': 50.0,
            'created_at': 'Fri Jun 23 2023',
            'paid_by_user_id': user1.id
        }), headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer TOKEN'
        })

        created_expense = Expense.query.filter_by(couple_id=user1.couple_id).first()
        assert response.status_code == 200
        assert response.json['expense']['id'] == created_expense.id
