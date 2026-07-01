"""
Validation service.

Provides reusable validation and normalization for expense data.
"""

from __future__ import annotations

from datetime import datetime, date

from flask import current_app


class ValidationError(Exception):
    """Raised when validation fails."""


class ValidationService:
    """Validation utilities for expense-related data."""

    @staticmethod
    def validate_amount(amount: int) -> int:
        if amount <= 0:
            raise ValidationError("Amount must be greater than 0.")

        if amount > current_app.config["MAX_EXPENSE_AMOUNT"]:
            raise ValidationError("Amount exceeds the allowed limit.")

        return amount

    @staticmethod
    def validate_category(category: str) -> str:
        category = category.strip().lower()

        if not category:
            raise ValidationError("Category is required.")

        if len(category) > current_app.config["MAX_CATEGORY_LENGTH"]:
            raise ValidationError("Category is too long.")

        return category

    @staticmethod
    def validate_description(description: str | None) -> str:
        description = (description or "").strip()

        return description[: current_app.config["MAX_DESCRIPTION_LENGTH"]]

    @staticmethod
    def validate_date(expense_date: str) -> date:
        try:
            return datetime.strptime(
                expense_date,
                current_app.config["DEFAULT_DATE_FORMAT"],
            ).date()

        except ValueError as exc:
            raise ValidationError("Invalid date.") from exc

    @classmethod
    def validate_expense(
        cls,
        *,
        amount: int,
        category: str,
        description: str | None,
        expense_date: str,
    ) -> dict:
        """
        Validate and normalize expense data.
        """

        return {
            "amount": cls.validate_amount(amount),
            "category": cls.validate_category(category),
            "description": cls.validate_description(description),
            "date": cls.validate_date(expense_date),
        }
