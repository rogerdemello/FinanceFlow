"""CSV export utilities for Personal Finance Assistant."""
from __future__ import annotations
import csv
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .assistant import PersonalFinanceAssistant


def export_expenses_csv(assistant: PersonalFinanceAssistant, output_path: str) -> None:
    """Export all expenses to CSV file.
    
    Args:
        assistant: PersonalFinanceAssistant instance
        output_path: Path to write CSV file
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Category', 'Amount'])
        for exp in assistant.expenses:
            writer.writerow([exp.date, exp.category, exp.amount])


def export_debts_csv(assistant: PersonalFinanceAssistant, output_path: str) -> None:
    """Export all debts to CSV file.
    
    Args:
        assistant: PersonalFinanceAssistant instance
        output_path: Path to write CSV file
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Balance', 'Interest Rate', 'Minimum Payment'])
        for name, debt in assistant.debt.items():
            writer.writerow([
                name,
                debt['balance'],
                debt['interest_rate'],
                debt['minimum_payment']
            ])


def import_expenses_csv(assistant: PersonalFinanceAssistant, input_path: str) -> int:
    """Import expenses from CSV file.
    
    Args:
        assistant: PersonalFinanceAssistant instance
        input_path: Path to CSV file
        
    Returns:
        Number of expenses imported
    """
    count = 0
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            assistant.log_expense(
                float(row['Amount']),
                row['Category']
            )
            count += 1
    return count


__all__ = ['export_expenses_csv', 'export_debts_csv', 'import_expenses_csv']
