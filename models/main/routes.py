#!/usr/bin/python3
"""
Module to handle main logic
"""
from flask import Blueprint, render_template
from flask_login import current_user
from models.Product import Product

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    """
    Home route

    Returns:
        render home template
    """
    if not current_user.is_authenticated:
        return render_template("home_page.html")
    elif current_user.user_type == "seller":
        products = Product.query.filter_by(user_id=current_user.id).all()
        return render_template("sellers/home_page.html", title="Sellers", products=products)
    elif current_user.user_type == "buyer":
        products = Product.query.all()
        return render_template("buyers/home_page.html", title="Buyers", products=products)


@main.route("/account")
def account():
    """
    Account route

    Returns:
        render account template
    """
    if not current_user.is_authenticated:
        return render_template("home_page.html")
    elif current_user.user_type == "seller":
        return render_template("sellers/account.html", title=current_user.fullname)
    elif current_user.user_type == "buyer":
        return render_template("buyers/account.html", title=current_user.fullname)
