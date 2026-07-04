"""
Application factory for ExpenseIQ.

This module creates and configures the Flask application instance,
initializes extensions, and registers blueprints.
"""

from __future__ import annotations
from app.utils.logger import configure_logger

from flask import Flask

from config import Config
from app.models import db


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """

    configure_logger()

    app = Flask(__name__)

    # Load Configuration

    app.config.from_object(Config)

    # Initialize Extensions

    db.init_app(app)

    # Register Blueprints

    from app.routes.main import main_bp
    from app.routes.expense import expense_bp
    from app.routes.budget import budget_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(budget_bp)

    from app.errors import register_error_handlers

    register_error_handlers(app)

    # Create Database

    with app.app_context():
        db.create_all()

    return app
