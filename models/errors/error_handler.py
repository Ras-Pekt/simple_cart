#!/usr/bin/python3
"""
Error handling module
"""
from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(403)
def forbidden(error):
    """
    Forbidden route
    
    Args:
        error: error message
    Returns:
        render forbidden template
    """
    return render_template("errors/forbidden.html", title="403 - Access Denied!"), 403


@errors.app_errorhandler(404)
def not_found(error):
    """
    Not found route

    Args:
        error: error message
    Returns:
        render not found template
    """
    return render_template("errors/not_found.html", title="404 - Not Found!"), 404


@errors.app_errorhandler(500)
def server_error(error):
    """
    Server error route

    Args:
        error: error message
    Returns:
        render server error template
    """
    return render_template("errors/server_error.html", title="500 - Server Error!"), 500
