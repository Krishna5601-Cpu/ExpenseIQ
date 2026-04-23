from flask import Blueprint, request, redirect, render_template
from datetime import datetime

from app.services.expense_service import (
    add_expense,
    get_expense_by_id,
    update_expense,
    delete_expense,
)

from app.services.validation_service import validate_expense_data

expense_bp = Blueprint("expense", __name__)


@expense_bp.route("/add-expense", methods=["POST"])
def create_expense():
    date = request.form.get("date")

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    category = request.form.get("category", "").strip().lower()

    if category == "custom":
        category = request.form.get(
            "custom_category", ""
        ).strip().lower()

    try:
        amount = int(request.form.get("amount", 0))
    except ValueError:
        return "Error: Invalid amount"

    errors = validate_expense_data(amount, category, date)

    if errors:
        return f"Error: {errors[0]}"

    data = {
        "amount": amount,
        "category": category,
        "description": request.form.get(
            "description", ""
        ).strip()[:100],
        "date": date,
    }

    add_expense(data)

    return redirect("/")


@expense_bp.route("/edit/<int:expense_id>")
def edit_page(expense_id):
    expense = get_expense_by_id(expense_id)

    if not expense:
        return "Expense not found"

    return render_template("edit.html", expense=expense)


@expense_bp.route("/update/<int:expense_id>", methods=["POST"])
def update(expense_id):
    category = request.form.get("category", "").strip().lower()
    date = request.form.get("date")

    try:
        amount = int(request.form.get("amount", 0))
    except ValueError:
        return "Error: Invalid amount"

    errors = validate_expense_data(amount, category, date)

    if errors:
        return f"Error: {errors[0]}"

    data = {
        "amount": amount,
        "category": category,
        "description": request.form.get(
            "description", ""
        ).strip()[:100],
        "date": date,
    }

    update_expense(expense_id, data)

    return redirect("/")


@expense_bp.route("/delete/<int:expense_id>")
def delete(expense_id):
    delete_expense(expense_id)
    return redirect("/")