"""Test CSV export/import functionality."""

from src.pfa.assistant import PersonalFinanceAssistant
from src.pfa.export import export_expenses_csv, export_debts_csv, import_expenses_csv
import tempfile
import os


def test_export_expenses():
    """Test exporting expenses to CSV."""
    assistant = PersonalFinanceAssistant()
    assistant.log_expense(100, "Groceries")
    assistant.log_expense(50, "Dining")

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        path = f.name

    try:
        export_expenses_csv(assistant, path)
        assert os.path.exists(path)

        with open(path, "r") as f:
            lines = f.readlines()
            assert len(lines) == 3  # header + 2 rows
            assert "Groceries" in lines[1]
            assert "100" in lines[1]
    finally:
        os.unlink(path)


def test_export_debts():
    """Test exporting debts to CSV."""
    assistant = PersonalFinanceAssistant()
    assistant.manage_debt("CreditCard", 1500, 18.5, 50)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        path = f.name

    try:
        export_debts_csv(assistant, path)
        assert os.path.exists(path)

        with open(path, "r") as f:
            lines = f.readlines()
            assert len(lines) == 2  # header + 1 row
            assert "CreditCard" in lines[1]
    finally:
        os.unlink(path)


def test_import_expenses():
    """Test importing expenses from CSV."""
    assistant = PersonalFinanceAssistant()

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        f.write("Date,Category,Amount\n")
        f.write("2025-12-19,Food,25.50\n")
        f.write("2025-12-18,Transport,15.00\n")
        path = f.name

    try:
        count = import_expenses_csv(assistant, path)
        assert count == 2
        assert len(assistant.expenses) == 2
        summary = assistant.expense_summary()
        assert summary["total_spent"] == 40.50
    finally:
        os.unlink(path)
