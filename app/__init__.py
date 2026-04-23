from flask import Flask
from config import Config
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes.main import main_bp
    from app.routes.expense import expense_bp
    from app.routes.budget import budget_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(budget_bp)

    return app
