#!/usr/bin/python3
"""
Module to handle the app's configurations logic
"""
from dotenv import load_dotenv
from os import environ

load_dotenv()


class Config:
    """
    App's Config class
    """
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
