from flask import Blueprint, jsonify, request, url_for

from backend.models import User, Couple
from backend.routes.auth_middleware import login_required
from backend.services import PartnerInviteService

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/test', methods=['GET'])
def test():
    return {"message": "Hello World"}


@api_bp.route('/expenses', methods=['GET'])
@login_required
def get_expenses(current_user: User):
    expenses = current_user.couple.expenses
    json_expenses = []
    for expense in expenses:
        json_expenses.append(expense.json())
    return jsonify({'expenses': json_expenses})



@api_bp.route('/partner_link', methods=['GET'])
@login_required
def partner_link(current_user: User):
    token = PartnerInviteService.generate_invite_token(current_user.id)
    link = f"http://localhost:3000/join/{token}"
    return jsonify({'link': link})


@api_bp.route('/join/<code>', methods=['GET'])
def join(code):
    user_id = PartnerInviteService.decode_invite_token(code)
    signed_up_user = User.query.filter_by(id=user_id).first()
    return jsonify({'user1': signed_up_user.json()})


@api_bp.route('/create_couple', methods=['POST'])
def create_couple():
    data = request.get_json()
    user1 = User.query.filter_by(id=data['user1_id']).first()
    user2 = User.query.filter_by(id=data['user2_id']).first()
    new_couple = Couple().create()
    user1.join_couple(new_couple.id)
    user2.join_couple(new_couple.id)
    return jsonify(new_couple.json())
