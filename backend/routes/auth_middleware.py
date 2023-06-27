from functools import wraps

from flask import request

from backend.models import User
from backend.services import JwtService


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing",
                "error": "Unauthorized"
            }, 401
        try:
            user_id = JwtService.decode_token(token)
            current_user = User.query.filter_by(id=user_id).first()

            if current_user is None:
                return {
                    "message": "Invalid Authentication token",
                    "error": "Unauthorized"
                }, 401

            return f(current_user, *args, **kwargs)
        except Exception as e:
            return {
                "message": "Invalid Authentication token",
                "error": e.args
            }, 401

    return wrap
