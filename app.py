from flask import Flask, request, jsonify, render_template, redirect
from config import Config
from services import add_expense, get_all_expenses, delete_expense
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def home():
    expenses = get_all_expenses()
    return render_template("index.html", expenses=expenses)


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


@app.route("/delete/<expense_id>")
def delete(expense_id):
    delete_expense(expense_id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
