import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_ai_insights(expenses):
    if not expenses:
        return ["No expenses available yet."]

    expense_data = []

    for e in expenses:
        expense_data.append(
            {
                "amount": e.amount,
                "category": e.category,
                "description": e.description,
                "date": e.date,
            }
        )

    system_prompt = """
You are ExpenseIQ AI, an intelligent personal finance analyst.

Your job:
- Analyze spending behavior
- Detect patterns
- Give practical saving advice
- Be concise
- Be accurate
- Be motivating
- Return 4 bullet insights only
- Mention currency as ₹
- No markdown
"""

    user_prompt = f"""
Analyze this expense data:

{json.dumps(expense_data, indent=2)}

Give:
1. Top spending trend
2. Wasteful pattern if any
3. Saving suggestion
4. Budget advice
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config={
            "system_instruction": system_prompt,
            "temperature": 0.4,
            "max_output_tokens": 250,
        },
    )

    text = response.text.strip()

    return text.split("\n")
