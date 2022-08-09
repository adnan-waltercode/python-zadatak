import jwt
from functools import wraps
from flask import request
from models import UserModel
from config import JWT_KEY

def decode_auth_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return{
                "message" : "Auth token missing",
                "error": "Unauthorized"
            }, 401
        try:
            jwtPayload = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
            user = UserModel.query.filter_by(email = jwtPayload['sub']).first()
            if user is None:
                return{
                    "message" : "Invalid token",
                    "error": "Unauthorized"
                }, 401
            kwargs['user'] = user.id
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return{
                    "message" : "Token expired",
                    "error": "Unauthorized"
                }, 401
        except jwt.InvalidTokenError:
            return{
                    "message" : "Invalid token",
                    "error": "Unauthorized"
                }, 401
    return decorated