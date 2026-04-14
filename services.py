import json
import os
import uuid
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime


FILE_PATH = "expenses.json"


def load_expenses():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_expenses(expenses):
    with open(FILE_PATH, "w") as f:
        json.dump(expenses, f, indent=4)


def add_expense(data):
    expenses = load_expenses()

    expense = {
        "id": str(uuid.uuid4()),
        "amount": data.get("amount"),
        "category": data.get("category"),
        "description": data.get("description"),
        "date": data.get("date"),
    }

    expenses.append(expense)
    save_expenses(expenses)

    return expense


def delete_expense(expense_id):
    expenses = load_expenses()

    updated_expenses = [expense for expense in expenses if expense["id"] != expense_id]

    save_expenses(updated_expenses)


def get_all_expenses():
    return load_expenses()


def get_expense_by_id(expense_id):
    expenses = load_expenses()

    for expense in expenses:
        if expense["id"] == expense_id:
            return expense

    return None


def update_expense(expense_id, data):
    expenses = load_expenses()

    for expense in expenses:
        if expense["id"] == expense_id:
            expense["amount"] = data.get("amount")
            expense["category"] = data.get("category")
            expense["description"] = data.get("description")
            expense["date"] = data.get("date")
            break

    save_expenses(expenses)


def generate_insights():
    expenses = load_expenses()

    if not expenses:
        return ["No data available"]

    insights = []

    # 🔥 Normalize + Prepare Data
    total = 0
    category_totals = defaultdict(int)
    daily_totals = defaultdict(int)

    for e in expenses:
        amount = int(e["amount"])
        category = e["category"].strip().lower()  # 🔥 normalize
        date = e["date"]

        total += amount
        category_totals[category] += amount
        daily_totals[date] += amount

    # 🔥 Total Spending
    insights.append(f"Total spending: ₹{total}")

    # 🔥 Category Percentage
    for cat, amt in category_totals.items():
        percent = (amt / total) * 100
        insights.append(f"{cat.title()} accounts for {percent:.1f}% of your spending")

    # 🔥 Highest Spending Category
    max_cat = max(category_totals, key=category_totals.get)
    insights.append(f"Your highest spending category is {max_cat.title()}")

    # 🔥 Average Daily Spending
    avg_daily = total / len(daily_totals)
    insights.append(f"Your average daily spending is ₹{avg_daily:.0f}")

    # 🔥 Spending Trend (simple)
    sorted_dates = sorted(daily_totals.keys())

    if len(sorted_dates) >= 2:
        first = daily_totals[sorted_dates[0]]
        last = daily_totals[sorted_dates[-1]]

        if last > first:
            insights.append("Your spending trend is increasing 📈")
        elif last < first:
            insights.append("Your spending trend is decreasing 📉")
        else:
            insights.append("Your spending trend is stable")

    return insights


def generate_advanced_insights():
    expenses = load_expenses()

    if not expenses:
        return ["No data available"]

    total = sum(e["amount"] for e in expenses)

    category_totals = defaultdict(int)

    for e in expenses:
        category_totals[e["category"]] += e["amount"]

    insights = []

    # Total
    insights.append(f"Total spending: ₹{total}")

    # Category %
    for cat, amt in category_totals.items():
        percent = (amt / total) * 100
        insights.append(f"{cat} accounts for {percent:.1f}%")

    # Highest category
    max_cat = max(category_totals, key=category_totals.get)
    insights.append(f"Highest spending: {max_cat}")

    return insights


def generate_pie_chart():
    expenses = load_expenses()

    if not expenses:
        return

    category_totals = {}

    for e in expenses:
        cat = e["category"]
        category_totals[cat] = category_totals.get(cat, 0) + e["amount"]

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%")

    plt.title("Expense Distribution")

    plt.savefig("static/pie_chart.png")
    plt.close()
