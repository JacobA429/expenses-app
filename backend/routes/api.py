from flask import Blueprint, jsonify, request, url_for

from backend.models import User, Couple
from backend.routes.auth_middleware import login_required
from backend.services import PartnerInviteService

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/test', methods=['GET'])
def test():
    return {"message": "Hello World"}

@api_bp.route('/user', methods=['GET'])
@login_required
def user(current_user: User):
    return jsonify(current_user.json())


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
    user1_id, user2_id = data['user1_id'], data['user2_id']
    new_couple = Couple(user1_id= user1_id, user2_id=user2_id)
    new_couple.create()
    return jsonify(new_couple.json())