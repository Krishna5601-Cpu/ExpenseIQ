"""
Budget routes.
"""

from flask import Blueprint, redirect, render_template, request

from app.services.budget_service import BudgetService

budget_bp = Blueprint("budget", __name__)


@budget_bp.get("/budget")
def budget_page():
    """
    Display the budget dashboard.
    """

    return render_template(
        "budget.html",
        budgets=BudgetService.load(),
    )


@budget_bp.post("/save-budget")
def save_budget():
    """
    Save budget configuration.
    """

    def to_int(value: str | None) -> int:
        try:
            return max(0, int(value or 0))
        except ValueError:
            return 0

    budget_data = {
        "overall": to_int(request.form.get("overall")),
        "categories": {
            "food": to_int(request.form.get("food")),
            "travel": to_int(request.form.get("travel")),
            "bills": to_int(request.form.get("bills")),
        },
    }

    BudgetService.save(budget_data)

    return redirect("/budget")
