from datetime import datetime


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