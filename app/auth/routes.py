from flask import redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user
from app import login_manager
from . import auth_bp
from .models import User

@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.get_by_username(username)
    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid username or password"}), 401
    
    login_user(user)
    token = user.generate_auth_token()
    return jsonify({"token": token.decode('utf-8')}), 200


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

