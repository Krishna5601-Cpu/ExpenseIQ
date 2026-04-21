import json
import os
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from models import db, Expense

BUDGET_FILE = "budgets.json"


def add_expense(data):
    expense = Expense(
        amount=data["amount"],
        category=data["category"],
        description=data["description"],
        date=data["date"],
    )
    db.session.add(expense)
    db.session.commit()
    return expense


def get_all_expenses():
    return Expense.query.order_by(Expense.id.desc()).all()


def get_expense_by_id(expense_id):
    return Expense.query.get(expense_id)


def update_expense(expense_id, data):
    expense = Expense.query.get(expense_id)

    if expense:
        expense.amount = data["amount"]
        expense.category = data["category"]
        expense.description = data["description"]
        expense.date = data["date"]
        db.session.commit()


def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)

    if expense:
        db.session.delete(expense)
        db.session.commit()


def generate_insights():
    expenses = get_all_expenses()
    budgets = load_budgets()

    if not expenses:
        return ["No data available"]

    insights = []
    total = 0
    category_totals = defaultdict(int)

    for e in expenses:
        amount = e.amount
        category = e.category.strip().lower()

        total += amount
        category_totals[category] += amount

    overall_budget = budgets.get("overall", 0)

    if overall_budget > 0:
        percent = (total / overall_budget) * 100

        if percent > 100:
            insights.append(
                f"🚨 You exceeded your overall budget by {percent - 100:.1f}%"
            )
        else:
            insights.append(f"✅ You used {percent:.1f}% of your overall budget")

    category_budgets = budgets.get("categories", {})

    for cat, amt in category_totals.items():
        budget = category_budgets.get(cat, 0)

        if budget > 0:
            percent = (amt / budget) * 100

            if percent > 100:
                insights.append(
                    f"🚨 {cat.title()} budget exceeded by {percent - 100:.1f}%"
                )
            else:
                insights.append(f"{cat.title()} usage: {percent:.1f}% of budget")

    if category_totals:
        max_cat = max(category_totals, key=category_totals.get)
        insights.append(f"Highest spending category: {max_cat.title()}")

    weekday_total = 0
    weekend_total = 0

    for e in expenses:
        date_obj = datetime.strptime(e.date, "%Y-%m-%d")

        if date_obj.weekday() >= 5:
            weekend_total += e.amount
        else:
            weekday_total += e.amount

    if weekend_total > weekday_total:
        insights.append("📅 You spend more on weekends")
    elif weekday_total > weekend_total:
        insights.append("📅 You spend more on weekdays")

    day_totals = defaultdict(int)

    for e in expenses:
        date_obj = datetime.strptime(e.date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A")
        day_totals[day_name] += e.amount

    if day_totals:
        max_day = max(day_totals, key=day_totals.get)
        insights.append(f"📊 Highest spending day: {max_day}")

    return insights


def generate_advanced_insights():
    expenses = get_all_expenses()

    if not expenses:
        return ["No data available"]

    total = sum(e.amount for e in expenses)
    category_totals = defaultdict(int)

    for e in expenses:
        category_totals[e.category] += e.amount

    insights = [f"Total spending: ₹{total}"]

    for cat, amt in category_totals.items():
        percent = (amt / total) * 100
        insights.append(f"{cat} accounts for {percent:.1f}%")

    max_cat = max(category_totals, key=category_totals.get)
    insights.append(f"Highest spending: {max_cat}")

    return insights


def generate_pie_chart():
    expenses = get_all_expenses()

    if not expenses:
        return

    category_totals = defaultdict(int)

    for e in expenses:
        category_totals[e.category] += e.amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.savefig("static/pie_chart.png")
    plt.close()


def generate_line_chart():
    expenses = get_all_expenses()

    if not expenses:
        return

    daily_totals = defaultdict(int)

    for e in expenses:
        daily_totals[e.date] += e.amount

    sorted_dates = sorted(daily_totals.keys())
    values = [daily_totals[d] for d in sorted_dates]

    plt.figure()
    plt.plot(sorted_dates, values, marker="o")
    plt.title("Spending Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()

    path = os.path.join("static", "line_chart.png")
    plt.savefig(path)
    plt.close()


def load_budgets():
    if not os.path.exists(BUDGET_FILE):
        return {"overall": 0, "categories": {}}

    try:
        with open(BUDGET_FILE, "r") as f:
            content = f.read().strip()

            if not content:
                return {"overall": 0, "categories": {}}

            return json.loads(content)

    except json.JSONDecodeError:
        return {"overall": 0, "categories": {}}


def save_budgets(data):
    with open(BUDGET_FILE, "w") as f:
        json.dump(data, f, indent=4)


def generate_description_insights():
    expenses = get_all_expenses()

    if not expenses:
        return []

    insights = []

    food_keywords = ["swiggy", "zomato", "pizza", "burger", "restaurant"]
    transport_keywords = ["uber", "ola", "metro", "petrol", "diesel"]
    subscription_keywords = ["netflix", "spotify", "prime", "youtube"]

    food_count = 0
    transport_count = 0
    sub_count = 0

    for e in expenses:
        desc = (e.description or "").lower()

        if any(word in desc for word in food_keywords):
            food_count += 1

        if any(word in desc for word in transport_keywords):
            transport_count += 1

        if any(word in desc for word in subscription_keywords):
            sub_count += 1

    if food_count >= 2:
        insights.append("🍔 Frequent food delivery / dining expenses detected")

    if transport_count >= 2:
        insights.append("🚕 Regular transport or fuel spending detected")

    if sub_count >= 1:
        insights.append("📺 Subscription expenses found")

    return insights


def validate_expense_data(amount, category, date):
    errors = []

    if amount <= 0:
        errors.append("Amount must be greater than 0")

    if amount > 1000000:
        errors.append("Amount too large")

    if not category.strip():
        errors.append("Category is required")

    if len(category) > 30:
        errors.append("Category too long")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        errors.append("Invalid date format")

    return errors
