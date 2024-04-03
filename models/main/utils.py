#!/usr/bin/python3
"""
Utility functions module
"""
from flask import url_for, current_app, flash, redirect, request
from flask_login import current_user, login_required
from flask_mail import Message
from functools import wraps
from models import mail
from PIL import Image
import phonenumbers
from secrets import token_hex
import os
import uuid


def generate_id():
    """
    Generate a unique id

    Returns:
        str: unique id
    """
    return str(uuid.uuid4())


def save_picture(form_picture, folder, size):
    """
    Save picture to file system

    Args:
        form_picture: picture file
        folder: folder to save picture
        size: picture size
    Returns:
        str: picture filename
    """
    hex = token_hex(8)
    _, ext = os.path.splitext(form_picture.filename)
    pic_filename = hex + ext
    pic_path = os.path.join(current_app.root_path, f"static/img/{folder}", pic_filename)

    new_size = size
    image = Image.open(form_picture)
    image.thumbnail(new_size)

    image.save(pic_path)
    return pic_filename


def send_password_reset_email(user):
    """
    Send password reset email

    Args:
        user: user object
    """
    token = user.reset_token()
    message = Message(
        "Request for Password Reset",
        sender="noreply@example.com",
        recipients=[user.email],
    )
    message.body = f'''To reset password, follow the link below

{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request, ignore this email.
'''

    mail.send(message)


def role_required(role):
    """
    Role required decorator

    Args:
        role: user role
    Returns:
        function: decorated function
    """
    def decorator(f):
        """
        Decorator function

        Args:
            f: function
        Returns:
            function: decorated function
        """
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            """
            Decorated function

            Args:
                *args: arguments
                **kwargs: keyword arguments
            Returns:
                function: decorated function
            """
            if not current_user.user_type == role:
                flash(
                    f"Sign up for a {role} account to access this page",
                    "danger"
                )
                return redirect(request.referrer or url_for('main.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def adjust_cart(cart_items, product_id, product):
    """
    Adjust cart items and gets total price of items in cart

    Args:
        cart_items: cart items in session
        product_id: product id
        product: product object
    Returns:
        total price of items in cart
    """
    cart_items[product_id]["name"] = product.name
    cart_items[product_id]["price"] = product.price

    total_price = 0
    for value in cart_items.values():
        total_price += value.get("price") * value.get("quantity")

    return total_price


def validate_phone_number(phone_number):
    """
    Validates a user's phone number

    Args:
        phone_number: user's phone number
    Returns:
        tuple: phone number and boolean value
    """
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if phonenumbers.is_valid_number(parsed_number):
            num = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            return (num, True)
        return (False, False)
    except phonenumbers.phonenumberutil.NumberParseException:
        return (False, False)