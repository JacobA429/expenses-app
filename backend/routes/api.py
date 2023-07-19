from datetime import datetime

from flask import Blueprint, jsonify, request, url_for

from backend.models import User, Couple, Expense
from backend.routes.auth_middleware import login_required
from backend.services import PartnerInviteService, UserBalanceCalculator

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/user/balance', methods=['GET'])
@login_required
def user_balance(current_user: User):
    expenses = current_user.couple.expenses
    balance = UserBalanceCalculator.balance_for_user(current_user, expenses)
    return jsonify({'balance': balance})

@api_bp.route('/couple', methods=['GET'])
@login_required
def couple(current_user: User):
    couple = current_user.couple
    return jsonify({'couple': couple.json()})

@api_bp.route('/user/current', methods=['GET'])
@login_required
def user(current_user: User):
    return jsonify({'user': current_user.json()})

@api_bp.route('/expenses/create', methods=['POST'])
@login_required
def create_expense(current_user: User):
    data = request.get_json()

    total, created_at, paid_by_user_id = data['total'], data['created_at'], data['paid_by_user_id']
    title = data['title']
    expense = Expense(
        title=title,
        total=total,
        created_at=datetime.strptime(created_at, '%a %b %d %Y').date(),
        paid_by_user_id=paid_by_user_id,
        couple_id=current_user.couple_id
    ).create()

    return(jsonify({'expense': expense.json() }))




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


@api_bp.route('/couple/create', methods=['POST'])
def create_couple():
    data = request.get_json()
    user1 = User.query.filter_by(id=data['user1_id']).first()
    user2 = User.query.filter_by(id=data['user2_id']).first()
    new_couple = Couple().create()
    user1.join_couple(new_couple.id)
    user2.join_couple(new_couple.id)
    return jsonify(new_couple.json())
