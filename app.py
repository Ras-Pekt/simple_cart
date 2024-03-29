#!/usr/bin/python3
"""
This is the entry point for the simple_cart app
"""
from models import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
