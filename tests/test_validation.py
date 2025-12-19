"""Test error handling and validation."""

import pytest
from src.pfa.assistant import PersonalFinanceAssistant


def test_negative_income():
    """Test that negative income raises ValueError."""
    assistant = PersonalFinanceAssistant()
    with pytest.raises(ValueError, match="non-negative"):
        assistant.create_budget(-1000, 500)


def test_negative_expense():
    """Test that negative expense raises ValueError."""
    assistant = PersonalFinanceAssistant()
    with pytest.raises(ValueError, match="non-negative"):
        assistant.log_expense(-50, "Food")


def test_empty_category():
    """Test that empty category raises ValueError."""
    assistant = PersonalFinanceAssistant()
    with pytest.raises(ValueError, match="cannot be empty"):
        assistant.log_expense(50, "")


def test_negative_debt():
    """Test that negative debt values raise ValueError."""
    assistant = PersonalFinanceAssistant()
    with pytest.raises(ValueError, match="non-negative"):
        assistant.manage_debt("Card", -100, 5, 10)


def test_empty_debt_name():
    """Test that empty debt name raises ValueError."""
    assistant = PersonalFinanceAssistant()
    with pytest.raises(ValueError, match="cannot be empty"):
        assistant.manage_debt("", 100, 5, 10)


def test_negative_savings_goal():
    """Test that negative savings goal raises ValueError."""
    assistant = PersonalFinanceAssistant()
    with pytest.raises(ValueError, match="non-negative"):
        assistant.set_savings_goal("Vacation", -500, "2026-06-01")


def test_invalid_savings_percentage():
    """Test that invalid savings percentage raises ValueError."""
    assistant = PersonalFinanceAssistant()
    with pytest.raises(ValueError, match="between 0 and 1"):
        assistant.create_budget(5000, 3000, 1.5)


def test_whitespace_trimming():
    """Test that whitespace is properly trimmed."""
    assistant = PersonalFinanceAssistant()
    entry = assistant.log_expense(100, "  Food  ")
    assert entry.category == "Food"

    result = assistant.manage_debt("  Card  ", 1000, 5, 50)
    assert "  Card  " not in assistant.debt
    assert "Card" in assistant.debt
