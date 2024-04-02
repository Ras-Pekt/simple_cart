#!/usr/bin/python3
"""
App initialization module
"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from models.Config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config=Config):
    """
    Create app instance
    
    Args:
        config: configuration object
    Returns:
        app instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from models.auth.auth_routes import auth
    from models.main.routes import main
    from models.products.product_routes import products
    from models.cart.cart_routes import cart
    from models.orders.order_routes import orders
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(products)
    app.register_blueprint(cart)
    app.register_blueprint(orders)

    return app
