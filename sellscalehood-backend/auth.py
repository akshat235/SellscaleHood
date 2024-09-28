from flask import Blueprint, request, jsonify
from models import db, User 
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY


bcrypt = Bcrypt()

auth_blueprint = Blueprint('auth', __name__)

def generate_token(user_id):
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24) 
    }, SECRET_KEY, algorithm='HS256')
    return token

# User registration
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username)
    new_user.set_password(password)  
    db.session.add(new_user)
    db.session.commit()
    token = generate_token(new_user.id)
    return jsonify({'message': 'User registered successfully', 'token': token}), 201

# User login
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    # If the user exists and the password is correct, generate a JWT token
    if user and user.check_password(password):
        token = generate_token(user.id)
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

