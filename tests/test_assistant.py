from src.pfa.assistant import PersonalFinanceAssistant


def test_budget_and_expense_flow():
    a = PersonalFinanceAssistant()
    out = a.create_budget(4000, 2000)
    assert out["recommended_savings"] == 400.0
    entry = a.log_expense(100, "Dining")
    s = a.expense_summary()
    assert s["total_spent"] == 100
    a.manage_debt("Card", 1000, 15, 20)
    plan = a.debt_payoff_plan()
    assert "Card" in plan[0]
