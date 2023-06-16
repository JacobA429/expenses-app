from flask import Blueprint, jsonify, request, url_for

from backend.models import User
from backend.routes.auth_middleware import login_required
from backend.services import PartnerInviteService

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/user', methods=['GET'])
@login_required
def user(current_user: User):
    return jsonify(current_user.json())


@api_bp.route('/partner_link', methods=['GET'])
@login_required
def partner_link(current_user: User):
    token = PartnerInviteService.generate_invite_token(current_user.id)
    link = f"{request.root_url}api/invite/{token}"
    return jsonify({'partner_link': link})
