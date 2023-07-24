from datetime import datetime

from flask import Blueprint, jsonify, request, url_for

from backend.models import User, Couple, Expense
from backend.routes.auth_middleware import login_required
from backend.services import PartnerInviteService, UserBalanceCalculator

api_bp = Blueprint('api', __name__, url_prefix='/api')


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