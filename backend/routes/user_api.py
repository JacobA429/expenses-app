from flask import Blueprint, jsonify
from backend.routes.auth_middleware import login_required
from backend.models import User
from backend.services import  UserBalanceCalculator


user_api_bp = Blueprint('user_api', __name__, url_prefix='/api/user')

@user_api_bp.route('/balance', methods=['GET'])
@login_required
def user_balance(current_user: User):
    expenses = current_user.couple.expenses
    balance = UserBalanceCalculator.balance_for_user(current_user, expenses)
    return jsonify({'balance': balance})


@user_api_bp.route('/current', methods=['GET'])
@login_required
def user(current_user: User):
    return jsonify({'user': current_user.json()})