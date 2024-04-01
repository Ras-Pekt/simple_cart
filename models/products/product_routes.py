#!/usr/bin/python3
"""
Routes for products module
"""
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from models import db
from models.main.utils import save_picture, role_required
from models.Product import Product
from models.products.product_forms import NewProduct


products = Blueprint("products", __name__)

@products.route("/product/new", methods=["GET", "POST"])
@login_required
@role_required("seller")
def new_product():
    """
    Add a new product route

    Returns:
        render new product template
    """
    form = NewProduct()

    if form.validate_on_submit():

        name = form.name.data
        description = form.description.data
        price = form.price.data
        picture = save_picture(form.picture.data, "product_pics", (300, 300))
        category = form.category.data
        quantity = form.quantity.data

        new_product = Product(
            name=name,
            description=description,
            price=price,
            picture=picture,
            category=category,
            quantity=quantity,
            user_id=current_user.id
        )

        db.session.add(new_product)
        db.session.commit()

        flash("Product added successfully", "success")
        return redirect(url_for("main.home"))

    return render_template("sellers/new_product.html", title="New Product", legend="New Product", form=form)


@products.route("/product/<string:product_id>")
def product(product_id):
    """
    Display a product route

    Args:
        product_id: product id
    Returns:
        render product template
    """
    product = Product.query.get_or_404(product_id)
    return render_template("sellers/product.html", title=product.name, product=product)


@products.route("/product/<string:product_id>/update", methods=["GET", "POST"])
@login_required
@role_required("seller")
def update_product(product_id):
    """
    Update a product route

    Args:
        product_id: product id
    Returns:
        render update product template
    """
    product = Product.query.get_or_404(product_id)

    if product.user_id != current_user.id:
        abort(403)

    form = NewProduct()

    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.category = form.category.data
        product.quantity = form.quantity.data
        product.picture = save_picture(form.picture.data, "product_pics", (300, 300))

        db.session.commit()
        flash("Product updated successfully", "success")
        return redirect(url_for("products.product", product_id=product.id))

    elif request.method == "GET":
        form.name.data = product.name
        form.description.data = product.description
        form.price.data = product.price
        form.category.data = product.category
        form.quantity.data = product.quantity

    return render_template("sellers/new_product.html", title="Update Product", legend="Update Product", form=form)


@products.route("/product/<string:product_id>/delete", methods=["POST"])
@login_required
@role_required("seller")
def delete_product(product_id):
    """
    Delete a product route

    Args:
        product_id: product id
    Returns:
        redirect to home page
    """
    product = Product.query.get_or_404(product_id)

    if product.user_id != current_user.id:
        abort(403)

    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully", "success")
    return redirect(url_for("main.home"))
