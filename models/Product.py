#!/usr/bin/python3
"""
Product database module
"""

from models import db
from models.main.utils import generate_id

class Product(db.Model):
    """
    Product database model
    """
    id = db.Column(db.String, primary_key=True, default=generate_id)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        """
        Product representation

        Returns:
            str: product id, product name and user id
        """
        return f"Product({self.id}, {self.name}, {self.user_id})"
