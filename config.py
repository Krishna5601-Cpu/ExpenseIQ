"""
Application configuration for ExpenseIQ.

This module centralizes all configurable settings used throughout the
application. Environment variables are loaded automatically, with
sensible defaults for local development.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Config:
    """Base configuration class."""

    # Flask

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key",
    )

    # -------------------------------------------------
    # Database
    # -------------------------------------------------

    INSTANCE_DIR = BASE_DIR / "instance"
    INSTANCE_DIR.mkdir(exist_ok=True)

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{INSTANCE_DIR / 'expenseiq.db'}",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gemini AI

    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    # Budget Storage

    BUDGET_FILE = BASE_DIR / "budgets.json"

    # Chart Output

    CHART_FOLDER: Path = BASE_DIR / "static"

    # Application

    MAX_DESCRIPTION_LENGTH: int = 100

    MAX_CATEGORY_LENGTH: int = 30

    MAX_EXPENSE_AMOUNT: int = 1_000_000

    DEFAULT_CURRENCY: str = "₹"

    DEFAULT_DATE_FORMAT: str = "%Y-%m-%d"
