# backend/app/app.py

from flask import Flask

from backend import db
from backend.routes import api_bp, auth_bp, user_api_bp, couple_api_bp
from flask_cors import CORS
from backend.config import DevelopmentConfig, TestingConfig, ProductionConfig


def create_app(config_name='development'):
    """Create the Flask application instance."""
    app = Flask(__name__)
    CORS(app)
    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        raise ValueError(f"Invalid configuration name: {config_name}")

    db.init_app(app)
    app.register_blueprint(api_bp)
    app.register_blueprint(user_api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(couple_api_bp)

    return app
