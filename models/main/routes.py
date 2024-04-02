#!/usr/bin/python3
"""
Module to handle main logic
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from models import bcrypt, db
from models.Product import Product
from models.User import User

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
        products = Product.query.order_by(Product.date_posted.desc()).all()
        return render_template("home_page.html", products=products)
    elif current_user.user_type == "seller":
        products = Product.query.filter_by(user_id=current_user.id).order_by(Product.date_posted.desc()).all()
        return render_template("sellers/home_page.html", title="Sellers", products=products)
    elif current_user.user_type == "buyer":
        products = Product.query.order_by(Product.date_posted.desc()).all()
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


@main.route("/search")
def search():
    """search functionality route"""
    search_term = request.args.get("search")

    if not current_user.is_authenticated or current_user.user_type == "buyer":
        products = Product.query.filter(Product.name.like(f"%{search_term}%")).all()
        if products is None:
            return render_template("buyers/search_results.html", title="Search Results", products=[])
        return render_template("buyers/search_results.html", title="Search Results", products=products)
    elif current_user.user_type == "seller":
        products = Product.query.filter(Product.name.like(f"%{search_term}%"), Product.user_id == current_user.id).all()
        if products is None:
            return render_template("sellers/search_results.html", title="Search Results", products=[])
        return render_template("sellers/search_results.html", title="Search Results", products=products)


@main.route('/change-password', methods=['POST'])
def change_password():
    user = User.query.get(current_user.id)
    
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not current_user.is_authenticated:
        flash('You must be logged in to change password', 'danger')
        return redirect(url_for('main.home'))

    if not bcrypt.check_password_hash(user.password, old_password):
        flash('Old password is incorrect', 'danger')
        return redirect(url_for('main.account'))

    if new_password != confirm_password:
        flash('New passwords do not match', 'danger')
        return redirect(url_for('main.account'))

    hash_pwd = bcrypt.generate_password_hash(new_password).decode("utf-8")
    user.password = hash_pwd
    db.session.commit()
    flash('Password changed successfully', 'success')
    return redirect(url_for('main.account'))
