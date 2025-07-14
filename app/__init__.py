# backend/app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db


# pip install flask flask-cors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)

    with app.app_context():
        # 注册蓝图
        from app.routes import pest_bp, chat_bp, auth_bp, detect_bp
        app.register_blueprint(pest_bp)
        app.register_blueprint(chat_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(detect_bp)
    @app.route('/')
    def hello():
        return 'Hello, Flask!'

    return app