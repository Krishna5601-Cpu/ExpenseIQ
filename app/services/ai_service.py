"""
AI service.

Generates AI-powered financial insights using Google Gemini.
"""

from __future__ import annotations

import json
import logging

from flask import current_app
from google import genai

from app.models import Expense

logger = logging.getLogger(__name__)


class AIService:
    """Service responsible for AI-generated financial insights."""

    @staticmethod
    def _client() -> genai.Client | None:
        api_key = current_app.config.get("GEMINI_API_KEY")

        if not api_key:
            return None

        return genai.Client(api_key=api_key)

    @staticmethod
    def _prepare_data(expenses: list[Expense]) -> list[dict]:
        return [
            {
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date": expense.date.isoformat(),
            }
            for expense in expenses
        ]

    @classmethod
    def generate_insights(
        cls,
        expenses: list[Expense],
    ) -> list[str]:
        """
        Generate AI financial insights.
        """

        if not expenses:
            return ["No expenses available yet."]

        client = cls._client()

        if client is None:
            return ["AI insights unavailable. Missing Gemini API key."]

        system_prompt = """
You are ExpenseIQ AI.

You are a professional financial advisor.

Analyze the user's spending habits carefully.

Return EXACTLY 4 detailed insights.

Rules:

- Each insight should be 60-120 words.
- Mention ₹ wherever applicable.
- Explain WHY you reached the conclusion.
- Give practical recommendations.
- Mention spending patterns.
- Mention categories if relevant.
- Be motivational.
- Do NOT use markdown.
- Do NOT use headings.
- Separate each insight using a blank line.
"""

        user_prompt = f"""
Expense Data:

{json.dumps(cls._prepare_data(expenses), indent=2)}

Generate exactly four insights:

1. Spending trend
2. Wasteful habit
3. Saving suggestion
4. Budget recommendation
"""

        try:
            response = client.models.generate_content(
                model=current_app.config["GEMINI_MODEL"],
                contents=user_prompt,
                config={
                    "system_instruction": system_prompt,
                    "temperature": 0.4,
                    "max_output_tokens": 250,
                },
            )

            text = response.text.strip()

            insights = []

            for line in text.splitlines():
                cleaned = line.strip().lstrip("-*•1234567890. ").strip()

                if cleaned:
                    insights.append(cleaned)

            if len(insights) == 1:
                insights = [
                    sentence.strip() for sentence in text.split(".") if sentence.strip()
                ]

            return insights[:4]

        except Exception:
            logger.exception("Failed to generate AI insights.")

            return ["AI insights are temporarily unavailable."]
