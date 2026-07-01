"""
Expense service.

Contains all database operations related to expenses.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.models import Expense, db

logger = logging.getLogger(__name__)


class ExpenseService:
    """
    Service class responsible for expense database operations.
    """

    @staticmethod
    def create(
        *,
        amount: int,
        category: str,
        description: str,
        expense_date: date,
    ) -> Expense:
        """
        Create a new expense.
        """

        expense = Expense(
            amount=amount,
            category=category,
            description=description,
            date=expense_date,
        )

        try:
            db.session.add(expense)
            db.session.commit()

            logger.info("Expense created successfully (id=%s)", expense.id)

            return expense

        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("Failed to create expense.")
            raise

    @staticmethod
    def get_all() -> List[Expense]:
        """
        Return all expenses ordered by newest first.
        """

        return Expense.query.order_by(Expense.date.desc(), Expense.id.desc()).all()

    @staticmethod
    def get_by_id(expense_id: int) -> Expense | None:
        """
        Return expense by ID.
        """

        return db.session.get(Expense, expense_id)

    @staticmethod
    def update(
        expense: Expense,
        *,
        amount: int,
        category: str,
        description: str,
        expense_date: date,
    ) -> Expense:
        """
        Update an existing expense.
        """

        try:
            expense.amount = amount
            expense.category = category
            expense.description = description
            expense.date = expense_date

            db.session.commit()

            logger.info(
                "Expense updated successfully (id=%s)",
                expense.id,
            )

            return expense

        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("Failed to update expense.")
            raise

    @staticmethod
    def delete(expense: Expense) -> None:
        """
        Delete an expense.
        """

        try:
            db.session.delete(expense)
            db.session.commit()

            logger.info(
                "Expense deleted successfully (id=%s)",
                expense.id,
            )

        except SQLAlchemyError:
            db.session.rollback()
            logger.exception("Failed to delete expense.")
            raise

    @staticmethod
    def get_total_amount() -> int:
        """
        Return total amount spent.
        """

        return sum(expense.amount for expense in Expense.query.all())

    @staticmethod
    def get_categories() -> list[str]:
        """
        Return all unique categories.
        """

        categories = (
            db.session.query(Expense.category)
            .distinct()
            .order_by(Expense.category)
            .all()
        )

        return [category for (category,) in categories]
