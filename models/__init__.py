#!/usr/bin/python3
"""
App initialization module
"""

from flask import Flask
from models.Config import Config


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

    return app
