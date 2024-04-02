#!/usr/bin/python3
"""
Module to handle cart logic
"""

from flask import Blueprint, session, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from models import db
from models.Cart import Cart
from models.main.utils import adjust_cart, role_required
from models.Order import Order
from models.Product import Product

cart = Blueprint("cart", __name__)


@cart.route("/cart")
@login_required
@role_required("buyer")
def view_cart():
    """
    View cart items route

    Returns:
        render cart template
    """
    cart_items = session.get(f"cart_{current_user.id}", {})
    return render_template("buyers/cart.html", title="Cart", cart_items=cart_items)


@cart.route("/add_to_cart/<string:product_id>")
@login_required
@role_required("buyer")
def add_to_cart(product_id):
    """
    Add product to cart route

    Args:
        product_id: product id
    Returns:
        redirect to home route
    """
    cart_items = session.get(f"cart_{current_user.id}", {})
    product = Product.query.get_or_404(product_id)

    if product_id in cart_items:
        cart_items[product_id] = {"quantity": cart_items[product_id]["quantity"] + 1}
    else:
        cart_items[product_id] = {"quantity": 1}

    session[f"total_price_{current_user.id}"] = adjust_cart(cart_items, product_id, product)

    session[f"cart_{current_user.id}"] = cart_items
    flash(
        "Product added to cart successfully",
        "success"
    )
    return redirect(url_for("main.home"))


@cart.route("/remove_from_cart/<string:product_id>")
@login_required
@role_required("buyer")
def remove_from_cart(product_id):
    """
    Removes product from cart route

    Args:
        product_id: product id
    Returns:
        redirect to cart route
    """
    product = Product.query.get_or_404(product_id)
    cart_items = session.get(f"cart_{current_user.id}", {})
    if product_id in cart_items:
        cart_items[product_id] = {"quantity": cart_items[product_id]["quantity"] - 1}

        session[f"total_price_{current_user.id}"] = adjust_cart(cart_items, product_id, product)

        if cart_items[product_id]["quantity"] == 0:
            cart_items.pop(product_id)
    session[f"cart_{current_user.id}"] = cart_items
    return redirect(url_for("cart.view_cart"))


@cart.route("/clear_cart")
@login_required
@role_required("buyer")
def clear_cart():
    """
    Clears cart route

    Returns:
        render cart template
    """
    session[f"cart_{current_user.id}"] = {}
    return render_template("buyers/cart.html", title="Cart", cart_items={})


@cart.route("/checkout")
@login_required
@role_required("buyer")
def checkout():
    """
    Checkout route
    Reduces the quantity of products in the product table
    Updates the order table
    Deletes cart items from cart table

    Returns:
        redirect to home route
    """
    cart_items = session.get(f"cart_{current_user.id}", {})

    # reduce product table by quantity in cart
    for product_id in cart_items:
        product = Product.query.get_or_404(product_id)
        product.quantity -= cart_items[product_id]["quantity"]

        if product.quantity == 0:
            db.session.delete(product)

        db.session.commit()
        
    # add to order table
    for key, value in cart_items.items():
        product_id = key
        name = value.get("name")
        price = value.get("price")
        quantity = value.get("quantity")
        user_id = current_user.id

        new_order = Order(
            product_id=product_id,
            name=name,
            price=price,
            quantity=quantity,
            user_id=user_id
        )

        db.session.add(new_order)
        db.session.commit()
    

    # delete cart items from cart table
    Cart.query.filter(Cart.user_id == current_user.id).delete()
    db.session.commit()

    flash(
        "Order placed successfully",
        "success"
    )

    session[f"cart_{current_user.id}"] = {}
    return redirect(url_for("main.home"))
