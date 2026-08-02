from __future__ import annotations

import json
import logging
from pydantic import BaseModel, Field
from flask import current_app
from google import genai
from google.genai import types

from app.models import Expense

logger = logging.getLogger(__name__)


# Schema for structured output enforcing 4 insights
class InsightsResponse(BaseModel):
    insights: list[str] = Field(
        ...,
        min_items=4,
        max_items=4,
        description="Exactly four detailed financial insights.",
    )


class AIService:
    """Service responsible for AI-generated financial insights."""

    # Updated default model to Gemini 3 Flash Preview
    DEFAULT_MODEL = "gemini-3-flash-preview"

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
        """Generate AI financial insights using Gemini 3 Flash Preview."""

        if not expenses:
            return ["No expenses available yet."]

        client = cls._client()

        if client is None:
            return ["AI insights unavailable. Missing Gemini API key."]

        model_name = current_app.config.get("GEMINI_MODEL", cls.DEFAULT_MODEL)

        system_prompt = """
You are ExpenseIQ AI, a professional financial advisor.
Analyze the user's spending habits carefully and return EXACTLY 4 detailed insights.

Insight topics required:
1. Overall spending trend
2. Identified wasteful habit
3. Concrete saving suggestion
4. Future budget recommendation

Rules:
- Each insight should be between 60-120 words.
- Mention ₹ (INR) wherever applicable.
- Explain WHY you reached each conclusion.
- Provide clear, actionable recommendations.
- Keep the tone encouraging and motivational.
- Plain text only (no markdown, no bolding, no headers within individual insights).
"""

        user_prompt = (
            f"Expense Data:\n{json.dumps(cls._prepare_data(expenses), indent=2)}"
        )

        try:
            # Configure structured output & thinking constraints for Gemini 3
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.4,
                max_output_tokens=2000,
                response_mime_type="application/json",
                response_schema=InsightsResponse,
                thinking_config=types.ThinkingConfig(
                    thinking_budget=1024  # Controls Gemini 3 reasoning depth for fast throughput
                ),
            )

            response = client.models.generate_content(
                model=model_name,
                contents=user_prompt,
                config=config,
            )

            # Gemini outputs guaranteed JSON matching InsightsResponse schema
            structured_data = json.loads(response.text)
            return structured_data.get("insights", [])

        except Exception:
            logger.exception("Failed to generate AI insights.")
            return ["AI insights are temporarily unavailable."]
