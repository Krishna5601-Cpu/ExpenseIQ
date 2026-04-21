from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Integer, nullable=False)

    category = db.Column(db.String(50), nullable=False)

    description = db.Column(db.String(150))

    date = db.Column(db.String(20), nullable=False)

