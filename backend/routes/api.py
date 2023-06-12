from flask import Blueprint, jsonify

from backend.models import User

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/users', methods=['GET'])
def get_users():
    user = User.query.get(1)
    return jsonify(user.json())