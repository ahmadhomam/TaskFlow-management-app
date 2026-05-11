from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_login import LoginManager
import os

load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)       # bound INSIDE create_app
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")


    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp,  url_prefix="/api/auth")

    with app.app_context():
        from app import models
        db.create_all()
    
    return app
