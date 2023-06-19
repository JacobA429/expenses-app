import json

import pytest

from backend.models import User, Couple


@pytest.mark.partner_link
class TestPartnerLink:
    user = None

    @pytest.fixture
    def mock_decode_token(self, mocker):
        # Mock JwtService.decode_token
        mock_token = mocker.patch('backend.services.JwtService.decode_token')
        mock_token.return_value = self.user.id

    @pytest.fixture
    def mock_generate_invite_token(self, mocker):
        # Mock JwtService.decode_token
        mock_token = mocker.patch('backend.services.PartnerInviteService.generate_invite_token')
        mock_token.return_value = "ABCD"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User(name='John Doe', email='john@example.com', password='password').create()

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

class TestJoin:
    user = None

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User(name='John Doe', email='john@example.com', password='password').create()

    @pytest.fixture
    def mock_decode_invite_token(self, mocker):
        # Mock JwtService.decode_token
        mock_token = mocker.patch('backend.services.PartnerInviteService.decode_invite_token')
        mock_token.return_value = self.user.id

    def test_join_returns_original_user(self, client, mock_decode_invite_token):
        response = client.get('/api/join/ABCD',
                              headers={
                                  'Content-Type': 'application/json',
                              }
                              )
        assert response.json['user1']['email'], 'john@example.com'

class TestCreateCouple:
    user1, user2 = None, None

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user1 = User(name='John Doe', email='john@example.com', password='password').create()
        self.user2 = User(name='Jane Doe', email='jane@example.com', password='password').create()

    def test_create_couple(self, client):
        response = client.post('/api/create_couple',
                               data=json.dumps({
                                   'user1_id': self.user1.id,
                                   'user2_id': self.user2.id
                               }),
                               headers={
                                   'Content-Type': 'application/json',
                               }
                               )

        couple_id = response.json['id']

        couple = Couple.query.filter_by(id=couple_id).first()
        assert couple_id is not None
        assert couple.user1.id == self.user1.id
        assert couple.user2.id == self.user2.id
