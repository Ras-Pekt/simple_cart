#!/usr/bin/python3
"""
Cart database module
"""
from models import db
from models.main.utils import generate_id


class Cart(db.Model):
    """
    Cart database model
    """
    id = db.Column(db.String, primary_key=True, default=generate_id)
    product_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        """
        Cart representation
        
        Returns:
            str: product id, quantity and user id
        """
        return f"Cart({self.product_id}, {self.quantity}, {self.user_id})"