from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def index():
    """Landing page - redirect to dashboard if logged in, else to login."""
    if current_user.is_authenticated:
        return redirect(url_for("views.dashboard"))
    return render_template("login.html")


@views_bp.route("/register")
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("views.dashboard"))
    return render_template("register.html")


@views_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)
