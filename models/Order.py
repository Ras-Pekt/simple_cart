#!/usr/bin/python3
"""
Order database module
"""
from models import db
from models.main.utils import generate_id


class Order(db.Model):
    """
    Order database model
    """
    id = db.Column(db.String, primary_key=True, default=generate_id)
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.String(255), db.ForeignKey('product.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """
        Order representation
        
        Returns:
            str: product id, price and quantity
        """
        return f"Order({self.product_id}, {self.price}, {self.quantity})"
