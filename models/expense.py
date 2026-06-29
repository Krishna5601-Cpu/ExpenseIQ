"""
Expense database model.
"""

from __future__ import annotations

from datetime import date, datetime

from . import db


class Expense(db.Model):
    """
    Represents a single expense transaction.
    """

    __tablename__ = "expenses"

    # Primary Key

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    # Expense Details

    amount = db.Column(
        db.Integer,
        nullable=False,
    )

    category = db.Column(
        db.String(30),
        nullable=False,
        index=True,
    )

    description = db.Column(
        db.String(100),
        nullable=True,
    )

    date = db.Column(
        db.Date,
        nullable=False,
        index=True,
    )

    # Audit Fields

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    # Utility Methods

    def to_dict(self) -> dict:
        """
        Convert model to dictionary.
        """

        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return (
            f"<Expense "
            f"id={self.id} "
            f"category='{self.category}' "
            f"amount={self.amount}>"
        )
