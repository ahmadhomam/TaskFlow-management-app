from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.
    Body: { "username": "...", "email": "...", "password": "..." }
    """
    data = request.get_json()

    # --- Validate input ---
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "username, email and password are required"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already taken"}), 409

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    # --- Create user ---
    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Log in with username + password.
    Body: { "username": "...", "password": "..." }
    """
    data = request.get_json()

    if not data or not all(k in data for k in ("username", "password")):
        return jsonify({"error": "username and password are required"}), 400

    user = User.query.filter_by(username=data["username"]).first()

    if user is None or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    login_user(user)   # stores user in session cookie
    return jsonify({"message": "Logged in", "user": user.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    """Return the currently logged-in user's info."""
    return jsonify({"user": current_user.to_dict()}), 200
