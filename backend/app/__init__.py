# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    from .routes import verification_routes
    app.register_blueprint(verification_routes)
    return app
