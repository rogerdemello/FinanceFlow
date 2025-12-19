"""Personal Finance Assistant module

Provides `PersonalFinanceAssistant` class for budgeting, expense tracking,
debt management, savings goals, and educational tips. Methods return
structured information suitable for use in CLI or integration with other apps.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import random

# Optional persistence
from .db import init_db, get_conn


@dataclass
class ExpenseEntry:
    amount: float
    category: str
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


class PersonalFinanceAssistant:
    """A small helper class to manage basic personal finance operations.

    Attributes
    ----------
    user_data: Dict[str, float]
        Stores top-level user metadata such as `income`, `expenses_total`, and
        `recommended_savings`.
    expenses: List[ExpenseEntry]
        Logged expense entries.
    debt: Dict[str, Dict[str, float]]
        Named debts with keys: `balance`, `interest_rate`, `minimum_payment`.
    savings_goals: Dict[str, Dict[str, str|float]]
        Savings goals keyed by name with `amount` and `target_date`.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.user_data: Dict[str, float] = {}
        self.expenses: List[ExpenseEntry] = []
        self.debt: Dict[str, Dict[str, float]] = {}
        self.savings_goals: Dict[str, Dict[str, str|float]] = {}

        self.db_path = db_path
        if self.db_path:
            try:
                init_db(self.db_path)
                self._load_from_db()
            except Exception:
                # If DB initialization fails, fall back to in-memory mode
                self.db_path = None

    def _load_from_db(self) -> None:
        """Load persisted records from the SQLite database into memory."""
        if not self.db_path:
            return
        conn = get_conn(self.db_path)
        cur = conn.cursor()

        cur.execute("SELECT amount, category, date FROM expenses ORDER BY id")
        rows = cur.fetchall()
        self.expenses = [ExpenseEntry(float(r[0]), r[1], r[2]) for r in rows]

        cur.execute("SELECT name, balance, interest, minimum FROM debts")
        rows = cur.fetchall()
        self.debt = {r[0]: {'balance': float(r[1]), 'interest_rate': float(r[2]), 'minimum_payment': float(r[3])} for r in rows}

        cur.execute("SELECT name, amount, target_date FROM savings_goals")
        rows = cur.fetchall()
        self.savings_goals = {r[0]: {'amount': float(r[1]), 'target_date': r[2]} for r in rows}

        cur.execute("SELECT income, expenses_total, recommended_savings FROM budget ORDER BY id DESC LIMIT 1")
        budget_row = cur.fetchone()
        if budget_row:
            self.user_data['income'] = float(budget_row[0])
            self.user_data['expenses_total'] = float(budget_row[1])
            self.user_data['recommended_savings'] = float(budget_row[2])

        conn.close()

    def create_budget(self, income: float, monthly_expenses_total: float, savings_percentage: float = 0.10) -> Dict[str, float]:
        """Calculate recommended savings and store budget metadata.

        Returns a dict with `income`, `expenses`, `recommended_savings` and `leftover`.
        """
        if income < 0 or monthly_expenses_total < 0:
            raise ValueError("Income and expenses must be non-negative")
        if not 0 <= savings_percentage <= 1:
            raise ValueError("Savings percentage must be between 0 and 1")
            
        recommended_savings = round(income * savings_percentage, 2)
        leftover = round(max(0.0, income - monthly_expenses_total - recommended_savings), 2)
        self.user_data['income'] = income
        self.user_data['expenses_total'] = monthly_expenses_total
        self.user_data['recommended_savings'] = recommended_savings
        
        # persist budget
        if self.db_path:
            try:
                conn = get_conn(self.db_path)
                cur = conn.cursor()
                cur.execute("INSERT INTO budget (income, expenses_total, recommended_savings, updated_at) VALUES (?, ?, ?, datetime('now'))",
                           (income, monthly_expenses_total, recommended_savings))
                conn.commit()
                conn.close()
            except Exception:
                pass  # fail gracefully
                
        return {
            'income': income,
            'expenses': monthly_expenses_total,
            'recommended_savings': recommended_savings,
            'leftover': leftover
        }

    def log_expense(self, amount: float, category: str) -> ExpenseEntry:
        """Log a single expense and return the created entry."""
        if amount < 0:
            raise ValueError("Expense amount must be non-negative")
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
            
        entry = ExpenseEntry(amount, category.strip())
        self.expenses.append(entry)
        # persist
        if self.db_path:
            try:
                conn = get_conn(self.db_path)
                cur = conn.cursor()
                cur.execute("INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)", (amount, category, entry.date))
                conn.commit()
                conn.close()
            except Exception:
                pass  # fail gracefully
        return entry

    def expense_summary(self) -> Dict[str, object]:
        """Return total spent and a breakdown by category."""
        total_spent = round(sum(e.amount for e in self.expenses), 2)
        by_category: Dict[str, float] = {}
        for e in self.expenses:
            by_category[e.category] = round(by_category.get(e.category, 0.0) + e.amount, 2)
        return {'total_spent': total_spent, 'by_category': by_category, 'count': len(self.expenses)}

    def reset_expenses(self, before_date: Optional[str] = None) -> Dict[str, int]:
        """Reset (delete) all expenses or expenses before a specific date.
        
        Args:
            before_date: Optional date string (YYYY-MM-DD). If provided, only delete
                        expenses before this date. If None, delete all expenses.
        
        Returns:
            Dict with count of deleted expenses.
        """
        if before_date:
            # Delete expenses before the given date
            original_count = len(self.expenses)
            self.expenses = [e for e in self.expenses if e.date >= before_date]
            deleted_count = original_count - len(self.expenses)
            
            # Persist to database
            if self.db_path:
                try:
                    conn = get_conn(self.db_path)
                    cur = conn.cursor()
                    cur.execute("DELETE FROM expenses WHERE date < ?", (before_date,))
                    conn.commit()
                    conn.close()
                except Exception:
                    pass  # fail gracefully
        else:
            # Delete all expenses
            deleted_count = len(self.expenses)
            self.expenses = []
            
            # Persist to database
            if self.db_path:
                try:
                    conn = get_conn(self.db_path)
                    cur = conn.cursor()
                    cur.execute("DELETE FROM expenses")
                    conn.commit()
                    conn.close()
                except Exception:
                    pass  # fail gracefully
        
        return {'deleted_count': deleted_count, 'remaining_count': len(self.expenses)}

    def manage_debt(self, debt_name: str, balance: float, interest_rate: float, minimum_payment: float) -> Dict[str, float]:
        """Add or update a debt entry and return total debt."""
        if balance < 0 or interest_rate < 0 or minimum_payment < 0:
            raise ValueError("Debt values must be non-negative")
        if not debt_name or not debt_name.strip():
            raise ValueError("Debt name cannot be empty")
            
        self.debt[debt_name.strip()] = {'balance': balance, 'interest_rate': interest_rate, 'minimum_payment': minimum_payment}
        # persist
        if self.db_path:
            try:
                conn = get_conn(self.db_path)
                cur = conn.cursor()
                cur.execute("INSERT OR REPLACE INTO debts (name, balance, interest, minimum) VALUES (?, ?, ?, ?)", (debt_name, balance, interest_rate, minimum_payment))
                conn.commit()
                conn.close()
            except Exception:
                pass  # fail gracefully

        total_debt = round(sum(d['balance'] for d in self.debt.values()), 2)
        return {'total_debt': total_debt}

    def debt_payoff_plan(self, method: str = 'avalanche') -> List[str]:
        """Return a simple payoff plan. `method` may be 'avalanche' or 'snowball'."""
        if not self.debt:
            return ['No debts recorded.']

        items = list(self.debt.items())
        if method == 'snowball':
            # Order by smallest balance
            items.sort(key=lambda x: x[1]['balance'])
        else:
            # Avalanche: order by highest interest rate
            items.sort(key=lambda x: x[1]['interest_rate'], reverse=True)

        plan = [f"Pay off {name}: ${d['balance']} at {d['interest_rate']}% (min ${d['minimum_payment']}/mo)" for name, d in items]
        return plan

    def set_savings_goal(self, goal_name: str, amount: float, target_date: str) -> Dict[str, object]:
        """Create or update a savings goal."""
        if amount < 0:
            raise ValueError("Goal amount must be non-negative")
        if not goal_name or not goal_name.strip():
            raise ValueError("Goal name cannot be empty")
            
        self.savings_goals[goal_name.strip()] = {'amount': amount, 'target_date': target_date}
        if self.db_path:
            try:
                conn = get_conn(self.db_path)
                cur = conn.cursor()
                cur.execute("INSERT OR REPLACE INTO savings_goals (name, amount, target_date) VALUES (?, ?, ?)", (goal_name, amount, target_date))
                conn.commit()
                conn.close()
            except Exception:
                pass  # fail gracefully
        return {'goal_name': goal_name, 'amount': amount, 'target_date': target_date}

    def savings_progress(self) -> List[str]:
        """Return a human-friendly list of current goals."""
        return [f"Goal: {k} — Target: ${v['amount']} by {v['target_date']}" for k, v in self.savings_goals.items()]

    def financial_education(self, topic: str) -> str:
        """Return a short list of resources for the given topic."""
        resources = {
            'budgeting': "Learn budgeting basics: https://www.consumerfinance.gov/learn/",
            'investing': "Beginner investing guides: https://www.investopedia.com/",
            'debt_management': "Debt management strategies: https://www.consumerfinance.gov/"
        }
        return resources.get(topic.lower(), "No curated resources for this topic yet.")

    def get_motivational_quote(self) -> str:
        quotes = [
            "Start where you are. Use what you have. Do what you can.",
            "The secret to getting ahead is getting started.",
            "Don’t watch the clock; do what it does. Keep going."
        ]
        return random.choice(quotes)


__all__ = ["PersonalFinanceAssistant", "ExpenseEntry"]
