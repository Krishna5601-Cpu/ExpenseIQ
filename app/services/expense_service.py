from app.models import db, Expense


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
