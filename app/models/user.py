from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    """微信用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(64), unique=True, nullable=False, comment='微信openid')
    unionid = db.Column(db.String(64), index=True, comment='微信unionid')
    nickname = db.Column(db.String(64), comment='昵称')
    avatar = db.Column(db.String(255), comment='头像URL')
    gender = db.Column(db.Integer, default=0, comment='0未知 1男 2女')
    country = db.Column(db.String(64), comment='国家')
    province = db.Column(db.String(64), comment='省份')
    city = db.Column(db.String(64), comment='城市')
    phone = db.Column(db.String(20), index=True, comment='手机号')
    status = db.Column(db.Integer, default=1, comment='0禁用 1正常')
    last_login = db.Column(db.DateTime, comment='最后登录时间')
    login_count = db.Column(db.Integer, default=0, comment='登录次数')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # 已移除所有密码相关字段和方法

    __table_args__ = (
        db.Index('idx_user_phone', phone),
        db.Index('idx_user_created', created_at),
    )

    def to_dict(self, include_sensitive=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'gender': self.gender,
            'country': self.country,
            'province': self.province,
            'city': self.city,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'login_count': self.login_count
        }
        if include_sensitive:
            data.update({
                'openid': self.openid,
                'unionid': self.unionid,
                'phone': self.phone
            })
        return data