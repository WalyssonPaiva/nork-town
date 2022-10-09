from flask import Blueprint, request
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import config
from datetime import datetime, timedelta
from ext import db

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/login', methods=['POST'])
def login():
    """Endpoint to login
    ---
    parameters:
        - in: body
          name: body
          schema:
            type: object
            properties:
              username:
                type: string
              password:
                type: string
    responses:
      200:
        description: A jwt token
        schema:
            token: string"""
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user is None:
        return {"message": "Invalid username"}, 401
    if check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
            },
            config.Config().SECRET_KEY)

        return {"token": token}

@user_routes.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return {"message": "Username already exists"}, 401
    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created successfully"}, 201
    
