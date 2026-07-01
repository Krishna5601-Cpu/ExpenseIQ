"""
Chart service.

Generates charts used by the dashboard.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from flask import current_app

from app.services.expense_service import ExpenseService


class ChartService:
    """Chart generation service."""

    @staticmethod
    def _chart_path(filename: str) -> Path:
        return current_app.config["CHART_FOLDER"] / filename

    @staticmethod
    def generate_pie_chart() -> None:
        """
        Generate expense distribution pie chart.
        """

        expenses = ExpenseService.get_all()

        if not expenses:
            return

        category_totals = defaultdict(int)

        for expense in expenses:
            category_totals[expense.category] += expense.amount

        plt.figure(figsize=(6, 6))

        plt.pie(
            category_totals.values(),
            labels=category_totals.keys(),
            autopct="%1.1f%%",
            startangle=90,
        )

        plt.title("Expense Distribution")
        plt.tight_layout()

        plt.savefig(
            ChartService._chart_path("pie_chart.png"),
            dpi=200,
            bbox_inches="tight",
        )

        plt.close()

    @staticmethod
    def generate_line_chart() -> None:
        """
        Generate spending trend line chart.
        """

        expenses = ExpenseService.get_all()

        if not expenses:
            return

        daily_totals = defaultdict(int)

        for expense in expenses:
            daily_totals[expense.date] += expense.amount

        dates = sorted(daily_totals.keys())
        values = [daily_totals[d] for d in dates]

        plt.figure(figsize=(8, 4))

        plt.plot(
            dates,
            values,
            marker="o",
            linewidth=2,
        )

        plt.title("Spending Trend")
        plt.xlabel("Date")
        plt.ylabel("Amount (₹)")
        plt.xticks(rotation=45)

        plt.grid(alpha=0.3)
        plt.tight_layout()

        plt.savefig(
            ChartService._chart_path("line_chart.png"),
            dpi=200,
            bbox_inches="tight",
        )

        plt.close()

    @classmethod
    def generate_all(cls) -> None:
        """
        Generate every dashboard chart.
        """

        cls.generate_pie_chart()
        cls.generate_line_chart()
