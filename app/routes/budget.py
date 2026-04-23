from flask import Blueprint, render_template, request, redirect

from app.services.budget_service import (
    load_budgets,
    save_budgets,
)

budget_bp = Blueprint("budget", __name__)


@budget_bp.route("/budget")
def budget_page():
    budgets = load_budgets()

    return render_template("budget.html", budgets=budgets)


@budget_bp.route("/save-budget", methods=["POST"])
def save_budget():
    try:
        overall = int(request.form.get("overall", 0))
    except ValueError:
        overall = 0

    categories = {
        "food": int(request.form.get("food", 0) or 0),
        "travel": int(request.form.get("travel", 0) or 0),
        "bills": int(request.form.get("bills", 0) or 0),
    }

    data = {"overall": overall, "categories": categories}

    save_budgets(data)

    return redirect("/budget")
