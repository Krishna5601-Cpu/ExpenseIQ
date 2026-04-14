import json
import os
import uuid

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