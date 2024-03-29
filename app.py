#!/usr/bin/python3
"""
This is the entry point for the simple_cart app
"""
from models import create_app, db

app = create_app()

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
