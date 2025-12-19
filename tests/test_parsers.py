from src.pfa.parsers import parse_expense_segments, parse_debt_segments


def test_parse_expense_segments():
    text = "50 groceries; 20 dining, 30 coffee"
    items = parse_expense_segments(text)
    assert len(items) == 3
    assert items[0][0] == 50
    assert items[0][1].lower() == 'groceries'
    assert items[2][1].lower() == 'coffee'


def test_parse_expense_no_category():
    items = parse_expense_segments("100")
    assert items[0][0] == 100
    assert items[0][1].lower() == 'misc'


def test_parse_debt_segments():
    text = "CreditCard 1500 18 50; StudentLoan 10000 5 100"
    debts = parse_debt_segments(text)
    assert len(debts) == 2
    assert debts[0][0] == 'CreditCard'
    assert debts[0][1] == 1500
    assert debts[1][2] == 5


def test_parse_debt_partial():
    debts = parse_debt_segments("Loan 5000 7")
    assert debts[0][0] == 'Loan'
    # incomplete numeric fields allowed -> balance parsed
    assert debts[0][1] == 5000
 