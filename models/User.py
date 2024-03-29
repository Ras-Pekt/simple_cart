#!/usr/bin/python3
"""
User database module
"""
from flask import current_app
from flask_login import UserMixin
from models import db, login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from models.main.utils import generate_id


@login_manager.user_loader
def load_user(user_id):
    """
    Load user by id

    Args:
        user_id: user id
    Returns:
        user object
    """
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    """
    User database model
    """
    id = db.Column(db.String, primary_key=True, default=generate_id)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)

    def reset_token(self):
        """
        Generate a token for password reset

        Returns:
            str: reset password token
        """
        ser = Serializer(current_app.config["SECRET_KEY"])
        return ser.dumps({"user_id": self.id})

    @staticmethod
    def verify_token(token):
        """
        Verify password reset token

        Args:
            token: token to verify
        Returns:
            user object
        """
        ser = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = ser.loads(token)["user_id"]
            return User.query.get(user_id)
        except Exception:
            return None


    def __repr__(self):
        """
        User representation
        
        Returns:
            str: user id, user name, user email, user type
        """
        return f"User({self.id}: {self.fullname}, {self.email}, {self.user_type})"
