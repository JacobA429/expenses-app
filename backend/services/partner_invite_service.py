from hashids import Hashids


class PartnerInviteService:
    _hashid = Hashids(min_length=8)

    @classmethod
    def generate_invite_token(cls, user_id):
        return cls._hashid.encode(user_id)

    @classmethod
    def decode_invite_token(cls, token):
        return cls._hashid.decode(token)[0]
