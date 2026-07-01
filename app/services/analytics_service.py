"""
Analytics service.

Generates insights and statistics from expense data.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date

from app.models import Expense
from app.services.budget_service import BudgetService
from app.services.expense_service import ExpenseService


class AnalyticsService:
    """Provides analytics and insights."""

    @staticmethod
    def category_totals() -> dict[str, int]:
        totals = defaultdict(int)

        for expense in ExpenseService.get_all():
            totals[expense.category] += expense.amount

        return dict(totals)

    @staticmethod
    def total_spending() -> int:
        return ExpenseService.get_total_amount()

    @staticmethod
    def category_percentages() -> dict[str, float]:
        totals = AnalyticsService.category_totals()
        overall = sum(totals.values())

        if overall == 0:
            return {}

        return {
            category: round((amount / overall) * 100, 1)
            for category, amount in totals.items()
        }

    @staticmethod
    def highest_category() -> str | None:
        totals = AnalyticsService.category_totals()

        if not totals:
            return None

        return max(totals, key=totals.get)

    @staticmethod
    def spending_by_day() -> dict[str, int]:
        result = defaultdict(int)

        for expense in ExpenseService.get_all():
            day = expense.date.strftime("%A")
            result[day] += expense.amount

        return dict(result)

    @staticmethod
    def spending_trend() -> dict[date, int]:
        trend = defaultdict(int)

        for expense in ExpenseService.get_all():
            trend[expense.date] += expense.amount

        return dict(sorted(trend.items()))

    @staticmethod
    def budget_insights() -> list[str]:
        budgets = BudgetService.load()
        expenses = ExpenseService.get_all()

        if not expenses:
            return ["No expense data available."]

        insights: list[str] = []

        total = sum(expense.amount for expense in expenses)
        overall_budget = budgets.get("overall", 0)

        if overall_budget > 0:
            percentage = (total / overall_budget) * 100

            if percentage > 100:
                insights.append(
                    f"🚨 Overall budget exceeded by {percentage - 100:.1f}%"
                )
            else:
                insights.append(f"✅ Overall budget usage: {percentage:.1f}%")

        category_totals = AnalyticsService.category_totals()

        for category, spent in category_totals.items():
            budget = budgets.get("categories", {}).get(category)

            if not budget:
                continue

            percentage = (spent / budget) * 100

            if percentage > 100:
                insights.append(
                    f"🚨 {category.title()} budget exceeded by {percentage - 100:.1f}%"
                )
            else:
                insights.append(f"{category.title()}: {percentage:.1f}% of budget used")

        return insights

    @staticmethod
    def description_insights() -> list[str]:
        expenses = ExpenseService.get_all()

        keywords = {
            "Food Delivery": [
                "zomato",
                "swiggy",
                "pizza",
                "burger",
                "restaurant",
            ],
            "Transport": [
                "uber",
                "ola",
                "metro",
                "petrol",
                "diesel",
            ],
            "Subscriptions": [
                "netflix",
                "spotify",
                "prime",
                "youtube",
            ],
        }

        counts = Counter()

        for expense in expenses:
            description = (expense.description or "").lower()

            for label, words in keywords.items():
                if any(word in description for word in words):
                    counts[label] += 1

        insights = []

        if counts["Food Delivery"] >= 2:
            insights.append("🍔 Frequent food delivery expenses detected.")

        if counts["Transport"] >= 2:
            insights.append("🚕 Regular transportation expenses detected.")

        if counts["Subscriptions"] >= 1:
            insights.append("📺 Subscription expenses detected.")

        return insights

    @staticmethod
    def advanced_insights() -> list[str]:
        expenses = ExpenseService.get_all()

        if not expenses:
            return ["No expense data available."]

        insights = []

        total = AnalyticsService.total_spending()
        highest = AnalyticsService.highest_category()
        percentages = AnalyticsService.category_percentages()
        weekdays = AnalyticsService.spending_by_day()

        insights.append(f"Total spending: ₹{total}")

        if highest:
            insights.append(f"Highest spending category: {highest.title()}")

        for category, percentage in percentages.items():
            insights.append(f"{category.title()} accounts for {percentage:.1f}%")

        if weekdays:
            busiest = max(weekdays, key=weekdays.get)
            insights.append(f"Highest spending day: {busiest}")

        return insights

    @staticmethod
    def all_insights() -> list[str]:
        return (
            AnalyticsService.advanced_insights()
            + AnalyticsService.budget_insights()
            + AnalyticsService.description_insights()
        )
