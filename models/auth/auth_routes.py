#!/usr/bin/python3
"""
Module to handle authentication logic
"""
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user
from models import db, bcrypt
from models.auth.auth_forms import (
    Register, LogIn, RequestPasswordReset, ResetPassword
)
from models.User import User
from models.main.utils import send_password_reset_email


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    New user registration route

    Returns:
        redirect to login route
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = Register()
    fullname = form.fullname.data
    email = form.email.data
    password = form.password.data
    phone_number = form.phonenumber.data
    user_type = form.usertype.data

    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(
            fullname=fullname, email=email, password=hash_pwd,
            phone_number=phone_number, user_type=user_type
        )

        db.session.add(new_user)
        db.session.commit()
        flash(
            f"{fullname.title()}'s account created successfully",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", title="Register", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in route

    Returns:
        redirect to home route
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LogIn()
    email = form.email.data
    password = form.password.data
    remember_me = form.remember.data

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=email).first()

        if existing_user and bcrypt.check_password_hash(
            existing_user.password, password
        ):
            login_user(existing_user, remember=remember_me)

            next_param = request.args.get("next")
            if next_param:
                return redirect(next_param)
            else:
                return redirect(url_for("main.home"))
        else:
            flash(
                "Log In Unsuccessful. Check Email and Password",
                "danger"
            )
    return render_template("auth/login.html", title="Login", form=form)


@auth.route("/logout")
def logout():
    """
    Log out route

    Returns:
        redirect to home route
    """
    logout_user()
    return redirect(url_for("main.home"))


@auth.route("/requestpasswordreset", methods=["GET", "POST"])
def request_password_reset():
    """
    Request password reset route

    Returns:
        redirect to login route
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RequestPasswordReset()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash(
            f"Instructions to reset password have been sent to {user.email}",
            "info"
        )
        return redirect("login")

    return render_template(
        "auth/request_password_reset.html",
        title="Request Password Reset", form=form
    )


@auth.route("/resetpassword/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Reset password route

    Args:
        token: reset password token
    Returns:
        redirect to login route
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    user = User.verify_token(token)
    if not user:
        flash(
            "That token is invalid or has expired",
            "warning"
        )
        return redirect(url_for("auth.request_password_reset"))

    form = ResetPassword()

    if form.validate_on_submit():
        hash_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hash_pwd
        db.session.commit()
        flash(
            "Your password has been successfully reset",
            "success"
        )
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/reset_password.html", title="Reset Password", form=form
    )
