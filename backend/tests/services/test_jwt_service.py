from backend.services.jwt_service import JwtService


def test_encode_token_returns_token(mocker):
    encode_mock = mocker.patch('jwt.encode')

    JwtService.encode_token(1)

    encode_mock.assert_called_once_with(
        {'exp': mocker.ANY, 'iat': mocker.ANY, 'sub': 1},
        'jwt_secret_key',
        algorithm='HS256'
    )


def test_decode_token_returns_payload():
    jwt = JwtService.encode_token(123)
    payload = JwtService.decode_token(jwt)

    assert payload is 123
