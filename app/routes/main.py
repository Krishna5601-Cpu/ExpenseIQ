from flask import Blueprint, render_template, jsonify

from app.services.expense_service import get_all_expenses
from app.services.analytics_service import (
    generate_advanced_insights,
    generate_insights,
    generate_description_insights,
    generate_pie_chart,
    generate_line_chart,
)
from app.services.ai_service import generate_ai_insights

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    expenses = get_all_expenses()

    insights = generate_advanced_insights()
    budget_insights = generate_insights()
    desc_insights = generate_description_insights()

    all_insights = insights + budget_insights + desc_insights

    generate_pie_chart()
    generate_line_chart()

    return render_template("index.html", expenses=expenses, insights=all_insights)


@main_bp.route("/ai-insights")
def ai_insights():
    expenses = get_all_expenses()

    data = generate_ai_insights(expenses)

    return jsonify({"insights": data})
