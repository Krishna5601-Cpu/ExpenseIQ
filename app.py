from flask import Flask, request, jsonify, render_template, redirect
from config import Config
from datetime import datetime

from services import (
    add_expense,
    get_all_expenses,
    delete_expense,
    get_expense_by_id,
    update_expense,
    generate_insights,
    generate_advanced_insights,
    generate_pie_chart,
    generate_line_chart,
    load_budgets,
    save_budgets,
)


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def home():
    expenses = get_all_expenses()

    insights = generate_advanced_insights()
    budget_insights = generate_insights()

    all_insights = insights + budget_insights

    generate_pie_chart()
    generate_line_chart()

    return render_template("index.html", expenses=expenses, insights=all_insights)


@app.route("/add-expense", methods=["POST"])
def create_expense():
    date = request.form.get("date")

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    category = request.form.get("category")

    if category == "custom":
        category = request.form.get("custom_category").strip().lower()

    data = {
        "amount": int(request.form.get("amount")),
        "category": category,
        "description": request.form.get("description"),
        "date": date,
    }

    add_expense(data)

    return redirect("/")


@app.route("/update/<expense_id>", methods=["POST"])
def update(expense_id):
    data = {
        "amount": int(request.form.get("amount")),
        "category": request.form.get("category"),
        "description": request.form.get("description"),
        "date": request.form.get("date"),
    }

    update_expense(expense_id, data)

    return redirect("/")


@app.route("/edit/<expense_id>")
def edit_page(expense_id):
    expense = get_expense_by_id(expense_id)
    return render_template("edit.html", expense=expense)


@app.route("/delete/<expense_id>")
def delete(expense_id):
    delete_expense(expense_id)
    return redirect("/")


@app.route("/budget")
def budget_page():
    budgets = load_budgets()
    return render_template("budget.html", budgets=budgets)


@app.route("/save-budget", methods=["POST"])
def save_budget():
    overall = int(request.form.get("overall", 0))

    categories = {
        "food": int(request.form.get("food", 0)),
        "travel": int(request.form.get("travel", 0)),
        "bills": int(request.form.get("bills", 0)),
    }

    data = {"overall": overall, "categories": categories}

    save_budgets(data)

    return redirect("/budget")


if __name__ == "__main__":
    app.run(debug=True)
