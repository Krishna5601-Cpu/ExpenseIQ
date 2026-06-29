"""
Database initialization and model exports.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .expense import Expense

__all__ = [
    "db",
    "Expense",
]
