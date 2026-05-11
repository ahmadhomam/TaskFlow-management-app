from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Flask-Login needs this to reload a user from the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """Stores registered users."""
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """Hash and store the password — never store plain text!"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


class Task(db.Model):
    """Stores tasks belonging to a user."""
    __tablename__ = "tasks"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    priority    = db.Column(db.String(20),  default="medium")   # low / medium / high
    status      = db.Column(db.String(20),  default="pending")  # pending / in_progress / completed
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "priority":    self.priority,
            "status":      self.status,
            "created_at":  self.created_at.strftime("%Y-%m-%d %H:%M"),
            "updated_at":  self.updated_at.strftime("%Y-%m-%d %H:%M"),
            "user_id":     self.user_id,
        }
