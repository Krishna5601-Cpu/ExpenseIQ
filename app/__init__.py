"""
Application factory for ExpenseIQ.
"""

from flask import Flask

from config import Config

from app.errors import register_error_handlers
from app.models import db
from app.routes.budget import budget_bp
from app.routes.expense import expense_bp
from app.routes.main import main_bp
from app.utils.logger import configure_logger


def create_app() -> Flask:
    """
    Create and configure the Flask application.
    """

    configure_logger()

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(budget_bp)

    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app
