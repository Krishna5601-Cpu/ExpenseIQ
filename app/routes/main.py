"""
Main application routes.
"""

from flask import Blueprint, jsonify, render_template

from app.services.ai_service import AIService
from app.services.analytics_service import AnalyticsService
from app.services.chart_service import ChartService
from app.services.expense_service import ExpenseService

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def home():
    """
    Dashboard.
    """

    expenses = ExpenseService.get_all()

    ChartService.generate_all()

    return render_template(
        "index.html",
        expenses=expenses,
        insights=AnalyticsService.all_insights(),
    )


@main_bp.get("/ai-insights")
def ai_insights():
    """
    Generate AI-powered financial insights.
    """

    expenses = ExpenseService.get_all()

    return jsonify(
        {
            "success": True,
            "insights": AIService.generate_insights(expenses),
        }
    )
