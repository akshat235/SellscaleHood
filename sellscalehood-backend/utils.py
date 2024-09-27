import jwt
from flask import request, current_app

def get_user_id_from_token():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return None
    try:
        token = token.split(" ")[1]
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded['user_id']
    except Exception:
        return None
