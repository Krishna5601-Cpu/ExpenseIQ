"""
Expense routes.
"""

from datetime import date

from flask import Blueprint, redirect, render_template, request

from app.services.expense_service import ExpenseService
from app.services.validation_service import (
    ValidationError,
    ValidationService,
)

expense_bp = Blueprint("expense", __name__)


@expense_bp.post("/add-expense")
def create_expense():
    """
    Create a new expense.
    """

    expense_date = request.form.get("date") or date.today().isoformat()

    category = request.form.get("category", "").strip()

    if category == "custom":
        category = request.form.get(
            "custom_category",
            "",
        ).strip()

    try:
        data = ValidationService.validate_expense(
            amount=int(request.form.get("amount", 0)),
            category=category,
            description=request.form.get("description"),
            expense_date=expense_date,
        )

        ExpenseService.create(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            expense_date=data["date"],
        )

    except (ValidationError, ValueError) as exc:
        return str(exc), 400

    return redirect("/")


@expense_bp.get("/edit/<int:expense_id>")
def edit_page(expense_id: int):
    """
    Render edit page.
    """

    expense = ExpenseService.get_by_id(expense_id)

    if expense is None:
        return "Expense not found.", 404

    return render_template(
        "edit.html",
        expense=expense,
    )


@expense_bp.post("/update/<int:expense_id>")
def update_expense(expense_id: int):
    """
    Update an expense.
    """

    expense = ExpenseService.get_by_id(expense_id)

    if expense is None:
        return "Expense not found.", 404

    expense_date = request.form.get("date") or date.today().isoformat()

    try:
        data = ValidationService.validate_expense(
            amount=int(request.form.get("amount", 0)),
            category=request.form.get("category", ""),
            description=request.form.get("description"),
            expense_date=expense_date,
        )

        ExpenseService.update(
            expense,
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            expense_date=data["date"],
        )

    except (ValidationError, ValueError) as exc:
        return str(exc), 400

    return redirect("/")


@expense_bp.get("/delete/<int:expense_id>")
def delete_expense(expense_id: int):
    """
    Delete an expense.
    """

    expense = ExpenseService.get_by_id(expense_id)

    if expense is None:
        return "Expense not found.", 404

    ExpenseService.delete(expense)

    return redirect("/")
