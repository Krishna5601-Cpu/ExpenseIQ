import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def generate_ai_insights(expenses):
    if not expenses:
        return ["No expenses available yet."]

    if not client:
        return ["AI insights unavailable. Missing API key."]

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
- Return exactly 4 short bullet insights
- Mention currency as ₹
- No markdown headings
- Keep output beginner-friendly
"""

    user_prompt = f"""
Analyze this expense data:

{json.dumps(expense_data, indent=2)}

Return:
1. Spending trend
2. Risk or wasteful habit
3. Savings suggestion
4. Budget recommendation
"""

    try:
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

        insights = [
            line.strip("-• ").strip() for line in text.split("\n") if line.strip()
        ]

        return insights[:4]

    except Exception:
        return [
            "AI insights temporarily unavailable.",
            "Please check API key or internet connection.",
        ]
