# app/routs/auth.py
from flask import Blueprint, request, jsonify, current_app
import requests
import jwt
import time
from datetime import timedelta
from app.extensions import db
from app.models.user import User
from app.utils.auth import token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/check_login', methods=['GET'])
@token_required
def check_login():
    """检查登录状态"""
    user = User.query.get(request.current_user_id)
    if not user:
        return jsonify({'code': 401, 'message': '用户不存在'}), 401

    return jsonify({
        'code': 200,
        'data': {
            'userInfo': user.to_dict()
        }
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """退出登录（前端只需清除token即可）"""
    return jsonify({'code': 200, 'message': '已退出'})


@auth_bp.route('/login', methods=['POST'])
def wechat_login():
    data = request.get_json()
    code = data.get('code')
    user_info = data.get('userInfo')

    if not code:
        return jsonify({'code': 400, 'message': '缺少code参数'}), 400

    # 获取微信openid
    wx_url = f'https://api.weixin.qq.com/sns/jscode2session?appid={current_app.config["WX_APPID"]}&secret={current_app.config["WX_SECRET"]}&js_code={code}&grant_type=authorization_code'

    try:
        wx_res = requests.get(wx_url, timeout=5)
        wx_data = wx_res.json()
        openid = wx_data.get('openid')

        if not openid:
            return jsonify({'code': 401, 'message': '微信登录失败'}), 401

        # 查找或创建用户（不再检查密码）
        user = User.query.filter_by(openid=openid).first()
        if not user:
            user = User(
                openid=openid,
                nickname=user_info.get('nickName'),
                avatar=user_info.get('avatarUrl'),
                gender=user_info.get('gender'),
                country=user_info.get('country'),
                province=user_info.get('province'),
                city=user_info.get('city')
            )
            db.session.add(user)
        else:
            # 更新用户信息
            user.nickname = user_info.get('nickName')
            user.avatar = user_info.get('avatarUrl')

        db.session.commit()

        # 生成token
        token = generate_jwt_token(user.id)

        return jsonify({
            'code': 200,
            'data': {
                'token': token,
                'userInfo': user.to_dict()
            }
        })

    except Exception as e:
        return jsonify({'code': 500, 'message': '服务器错误'}), 500

def generate_jwt_token(user_id):
    """生成JWT Token"""
    payload = {
        'user_id': user_id,
        'exp': int(time.time()) + 3600 * 24 * 7  # 7天过期
    }
    JWT_SECRET = current_app.config['JWT_SECRET']
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')