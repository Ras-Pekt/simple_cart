#!/usr/bin/python3
"""
Product form module
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FloatField
from wtforms.validators import DataRequired, NumberRange


class NewProduct(FlaskForm):
    """
    New product form

    Args:
        FlaskForm: Flask form class
    """
    name = StringField(
        "Product Name",
        validators=[
            DataRequired()
        ]
    )

    description = TextAreaField(
        "Product Description",
        validators=[
            DataRequired()
        ]
    )

    price = FloatField(
        "Product Price",
        validators=[
            DataRequired(),
            NumberRange(min=0.01, message="Price must be greater than 0.")
        ]
    )

    picture = FileField(
        "Upload Image(s) of the Product",
        validators=[
            DataRequired(),
            FileAllowed([
                "jpg",
                "jpeg",
                "png",
            ])
        ]
    )

    category = StringField(
        "Product Category",
        validators=[
            DataRequired()
        ]
    )

    quantity = IntegerField(
        "Product Quantity",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Quantity must be greater than 0.")
        ]
    )

    submit = SubmitField("Add Product")
