#!/usr/bin/python3
"""
Order form module
"""

from flask import Blueprint, render_template
from flask_login import current_user
from models import db
from models.Order import Order


orders = Blueprint("orders", __name__)


@orders.route("/orders")
def view_orders():
    """
    View orders route

    Returns:
        render orders template
    """
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template("buyers/orders.html", title="Purchase History", orders=orders)
