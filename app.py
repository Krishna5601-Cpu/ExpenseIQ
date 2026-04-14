from flask import Flask, request, jsonify, render_template, redirect
from config import Config
from services import (
    add_expense,
    get_all_expenses,
    delete_expense,
    get_expense_by_id,
    update_expense,
    generate_insights,
    generate_advanced_insights,
    generate_pie_chart,
)
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def home():
    expenses = get_all_expenses()
    insights = generate_advanced_insights()

    generate_pie_chart()

    return render_template("index.html", expenses=expenses, insights=insights)


@app.route("/add-expense", methods=["POST"])
def create_expense():
    date = request.form.get("date")

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    data = {
        "amount": int(request.form.get("amount")),
        "category": request.form.get("category"),
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


if __name__ == "__main__":
    app.run(debug=True)
