# backend/app/__init__.py
from flask import Flask
# pip install flask flask-cors

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello, Flask!'

    return app