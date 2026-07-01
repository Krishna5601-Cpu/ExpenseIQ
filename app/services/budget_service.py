"""
Budget service.

Handles loading and saving budget data from JSON storage.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from flask import current_app

logger = logging.getLogger(__name__)


class BudgetService:
    """Service responsible for budget persistence."""

    @staticmethod
    def load() -> dict[str, Any]:
        """
        Load budget data.

        Returns:
            Dictionary containing overall and category budgets.
        """

        budget_file: Path = current_app.config["BUDGET_FILE"]

        if not budget_file.exists():
            logger.info("Budget file not found. Using default values.")
            return BudgetService.default_budget()

        try:
            with budget_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            return BudgetService.validate(data)

        except json.JSONDecodeError:
            logger.exception("Budget JSON is corrupted.")

        except OSError:
            logger.exception("Unable to read budget file.")

        return BudgetService.default_budget()

    @staticmethod
    def save(data: dict[str, Any]) -> None:
        """
        Save budget data safely.

        Uses atomic write to prevent corruption.
        """

        budget_file: Path = current_app.config["BUDGET_FILE"]

        data = BudgetService.validate(data)

        try:
            with NamedTemporaryFile(
                "w",
                delete=False,
                encoding="utf-8",
            ) as temp:

                json.dump(
                    data,
                    temp,
                    indent=4,
                )

                temp_path = Path(temp.name)

            temp_path.replace(budget_file)

            logger.info("Budget saved successfully.")

        except OSError:
            logger.exception("Failed to save budget.")
            raise

    @staticmethod
    def validate(data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate budget structure.
        """

        if not isinstance(data, dict):
            return BudgetService.default_budget()

        return {
            "overall": int(data.get("overall", 0)),
            "categories": dict(data.get("categories", {})),
        }

    @staticmethod
    def default_budget() -> dict[str, Any]:
        """
        Return default budget structure.
        """

        return {
            "overall": 0,
            "categories": {},
        }
