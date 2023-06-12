import datetime

import jwt


class JwtService:
    
    secret_key = 'jwt_secret_key'
    @classmethod
    def encode_token(cls, subject):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=60),
            'iat': datetime.datetime.utcnow(),
            'sub': subject
        }
        return jwt.encode(payload,cls.secret_key, algorithm='HS256')

    @classmethod
    def decode_token(cls, token):
        payload =  jwt.decode(token, cls.secret_key, algorithms=["HS256"])
        return payload['sub']
