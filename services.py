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


from collections import defaultdict


def generate_insights():
    expenses = load_expenses()
    budgets = load_budgets()

    if not expenses:
        return ["No data available"]

    insights = []

    total = 0
    category_totals = defaultdict(int)

    for e in expenses:
        amount = int(e["amount"])
        category = e["category"].strip().lower()

        total += amount
        category_totals[category] += amount

    # Overall Budget Check
    overall_budget = budgets.get("overall", 0)

    if overall_budget > 0:
        percent = (total / overall_budget) * 100

        if percent > 100:
            insights.append(
                f"🚨 You exceeded your overall budget by {percent - 100:.1f}%"
            )
        else:
            insights.append(f"✅ You used {percent:.1f}% of your overall budget")

    # Category Budget Check
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

    # Highest category
    if category_totals:
        max_cat = max(category_totals, key=category_totals.get)
        insights.append(f"Highest spending category: {max_cat.title()}")

    print("Budgets:", budgets)
    print("Category totals:", category_totals)

    from datetime import datetime

    # Weekly + Weekend Analysis
    weekday_total = 0
    weekend_total = 0

    for e in expenses:
        date_obj = datetime.strptime(e["date"], "%Y-%m-%d")
        amount = int(e["amount"])

        # Monday=0 ... Sunday=6
        if date_obj.weekday() >= 5:  # Saturday, Sunday
            weekend_total += amount
        else:
            weekday_total += amount

    # Compare
    if weekend_total > weekday_total:
        insights.append("📅 You spend more on weekends")
    elif weekday_total > weekend_total:
        insights.append("📅 You spend more on weekdays")

    # Highest Spending Day
    day_totals = defaultdict(int)

    for e in expenses:
        date_obj = datetime.strptime(e["date"], "%Y-%m-%d")
        day_name = date_obj.strftime("%A")

        day_totals[day_name] += int(e["amount"])

    if day_totals:
        max_day = max(day_totals, key=day_totals.get)
        insights.append(f"📊 Highest spending day: {max_day}")

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


def generate_line_chart():
    expenses = load_expenses()

    if not expenses:
        return

    daily_totals = defaultdict(int)

    for e in expenses:
        date = e["date"]
        amount = int(e["amount"])
        daily_totals[date] += amount

    # Sort dates
    sorted_dates = sorted(daily_totals.keys())
    values = [daily_totals[d] for d in sorted_dates]

    plt.figure()
    plt.plot(sorted_dates, values, marker="o")

    plt.title("Spending Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount")

    plt.xticks(rotation=45)

    plt.tight_layout()

    import os

    path = os.path.join("static", "line_chart.png")
    plt.savefig(path)
    plt.close()


BUDGET_FILE = "budgets.json"


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
