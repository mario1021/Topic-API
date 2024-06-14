from flask import redirect, url_for, request, jsonify
from flask_jwt_extended import create_access_token 
from . import auth_bp
from .models import User

@auth_bp.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.get_by_username(username)
    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid username or password"}), 401
    
    access_token = create_access_token(identity=user.id)

    return jsonify(access_token=access_token), 200

#the signup route now
@auth_bp.route('/signup', methods=['POST'])
def signup():
    
    data=request.get_json()
    username = data.get('username')


    if User.get_by_username(username) is not None:
        return jsonify({"message": "User already exists"}), 409

    full_name = data.get('full_name')
    password = data.get('password')
    user = User(username, full_name)
    user.set_password(password)
    print(user.username)
    user.save()
    return jsonify({"message": "User created successfully"}), 201



def load_user(user_id):
    return User.get_by_id(user_id)

