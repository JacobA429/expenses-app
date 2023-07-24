from flask import Blueprint, jsonify, request
from backend.routes.auth_middleware import login_required
from backend.models import User, Couple

from backend.services import  UserBalanceCalculator


couple_api_bp = Blueprint('couple_api', __name__, url_prefix='/api/couple')

@couple_api_bp.route('/current', methods=['GET'])
@login_required
def couple(current_user: User):
    couple = current_user.couple
    return jsonify({'couple': couple.json()})

@couple_api_bp.route('/create', methods=['POST'])
def create_couple():
    data = request.get_json()
    user1 = User.query.filter_by(id=data['user1_id']).first()
    user2 = User.query.filter_by(id=data['user2_id']).first()
    new_couple = Couple().create()
    user1.join_couple(new_couple.id)
    user2.join_couple(new_couple.id)
    return jsonify(new_couple.json())