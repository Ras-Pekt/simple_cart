#!/usr/bin/python3
"""
Authentication forms module
"""

from flask_wtf import FlaskForm
from models.User import User
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class Register(FlaskForm):
    """
    New member registration class/form

    Args:
        FlaskForm: form class
    """
    fullname = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(min=5, max=50)
        ]
    )

    usertype = StringField(
        "User Type",
        validators=[
            DataRequired()
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=50)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    phonenumber = StringField(
        "Phone Number",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Register")

    def validate_email(self, email):
        """
        checks if the email already exists in the database

        Args:
            email: email address
        Raises:
            ValidationError: if email already exists
        """
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError(
                "This email already has an account associated with it"
            )


class LogIn(FlaskForm):
    """
    Existing member log in class/form

    Args:
        FlaskForm: form class
    """
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=50)
        ]
    )

    remember = BooleanField("Remember Me")

    submit = SubmitField("Log In")


class RequestPasswordReset(FlaskForm):
    """
    Request password reset class/form

    Args:
        FlaskForm: form class
    """
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """
        checks if the email already exists in the database

        Args:
            email: email address
        Raises:
            ValidationError: if email does not exist
        """
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email is None:
            raise ValidationError(
                "This email is not associated with an account. Please register"
            )


class ResetPassword(FlaskForm):
    """
    Reset password class/form

    Args:
        FlaskForm: form class
    """
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=50)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Reset Password")
