from flask import Blueprint, render_template

from app.services.expense_service import get_all_expenses
from app.services.ai_service import generate_ai_insights
from app.services.analytics_service import (
    generate_advanced_insights,
    generate_insights,
    generate_description_insights,
    generate_pie_chart,
    generate_line_chart,
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    expenses = get_all_expenses()

    insights = generate_advanced_insights()
    budget_insights = generate_insights()
    desc_insights = generate_description_insights()
    ai_insights = generate_ai_insights(expenses)

    all_insights = insights + budget_insights + desc_insights + ai_insights

    generate_pie_chart()
    generate_line_chart()

    return render_template("index.html", expenses=expenses, insights=all_insights)
