from functools import wraps
from flask import request
import config
import jwt
from src.models import User

def required_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if "Authorization" not in request.headers:
            return {"message": "Authorization header is missing"}, 401
        try:
            data = jwt.decode(request.headers["Authorization"], config.Config().SECRET_KEY, algorithms=['HS256'])
            user = User.query.filter_by(id=data['user_id']).first()
        except:
            return {"message": "Invalid token"}, 401
        return func(*args, **kwargs)
    return decorated
