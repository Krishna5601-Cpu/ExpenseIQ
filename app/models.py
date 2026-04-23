from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(150), nullable=True)
    date = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Expense {self.id} {self.category} ₹{self.amount}>"
