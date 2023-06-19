from flask import Blueprint, request, jsonify, make_response, render_template, redirect, url_for
from werkzeug.security import check_password_hash

from backend.models import User
from backend.services.jwt_service import JwtService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/signup', methods=['POST', 'GET'])
def signup_user():
    if request.method == 'GET':  # If the request is GET we return the
        # sign up page and forms
        return render_template('signup.html')
    data = request.get_json()
    email, password, name = data['email'], data['password'], data['name']
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return make_response('A user already exists with the email', 409)

    new_user = User(email=email, password=password, name=name)
    new_user.create()
    return make_response(jsonify(new_user.json()), 201)


@auth_bp.route('/login', methods=['POST', 'GET'])
def login_user():
    data = request.get_json()
    email, password = data['email'], data['password']
    if not email or not password:
        return make_response('Email or password missing', 401)

    user = User.query.filter_by(email=email).first()

    if not user:
        return make_response(jsonify({'message': 'No user with email found'}), 401)

    if not check_password_hash(user.password, password):
        return make_response(jsonify({'message': 'Could not verify email and password'}), 401)

    token = JwtService.encode_token(user.id)
    return make_response({'token': token}, 201)
