import json
import os

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
