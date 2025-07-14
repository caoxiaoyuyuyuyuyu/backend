# app/utils/auth.py
import jwt
from functools import wraps
from flask import request, jsonify

import app.config


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'code': 401, 'message': '缺少认证token'}), 401

        try:
            # 去掉可能的Bearer前缀
            if token.startswith('Bearer '):
                token = token[7:]
            JWT_SECRET = app.config.Config.JWT_SECRET
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'code': 401, 'message': 'token已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'code': 401, 'message': '无效token'}), 401

        return f(*args, **kwargs)

    return decorated_function