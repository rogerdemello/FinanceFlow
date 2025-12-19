"""Integrated AIML bot loader and runner with `PersonalFinanceAssistant`.

This module loads AIML files and provides a small interactive console that
also recognizes a few command-like inputs to call `PersonalFinanceAssistant`
methods (budget creation, logging expenses, adding debts, and summaries).

Dependencies: `aiml`, `textblob` (for a simple sentiment check).
"""
from __future__ import annotations
import os
import re
import aiml
from textblob import TextBlob

from .assistant import PersonalFinanceAssistant

AIML_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'aiml'))


def create_kernel(load_path: str | None = None) -> aiml.Kernel:
    import time
    # Compatibility shim: older PyAIML uses time.clock which was removed
    # in Python 3.8+. Provide a fallback to perf_counter to avoid crashes.
    if not hasattr(time, 'clock'):
        time.clock = time.perf_counter

    kernel = aiml.Kernel()
    load_path = load_path or AIML_DIR
    if not os.path.isdir(load_path):
        return kernel
    # Load all .aiml files in the aiml directory
    for fname in os.listdir(load_path):
        if fname.endswith('.aiml'):
            path = os.path.join(load_path, fname)
            kernel.learn(path)
    return kernel


def _sentiment_warn(text: str) -> None:
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity < -0.5:
            print("[Assistant] I detect some stress in your message — if this is about money, I can help create a calmer plan.")
    except Exception:
        # sentiment analysis is optional; silently ignore errors
        pass


def _parse_amount(token: str) -> float | None:
    try:
        return float(token.replace('$', '').replace(',', ''))
    except Exception:
        return None


def run_console():
    kernel = create_kernel()
    assistant = PersonalFinanceAssistant(db_path='data/db.sqlite3')
    
    print('='*60)
    print(' Personal Finance Assistant - Interactive Console')
    print('='*60)
    print()
    print('Type "help" for commands or "quit" to exit.')
    print('State is persisted to data/db.sqlite3')
    print()
    
    while True:
        try:
            text = input('\n💰 > ')
        except (EOFError, KeyboardInterrupt):
            print('\n👋 Goodbye!')
            break
        if not text:
            continue
        if text.strip().lower() in ('quit', 'exit'):
            print('👋 Goodbye!')
            break

        _sentiment_warn(text)

        low = text.strip().lower()

        # Budget creation: "Income 4000 Expenses 2500"
        if low.startswith('income') and 'expenses' in low:
            parts = re.findall(r"[-+]?[0-9]*\.?[0-9]+", text)
            if len(parts) >= 2:
                income = _parse_amount(parts[0])
                expenses = _parse_amount(parts[1])
                if income is not None and expenses is not None:
                    try:
                        out = assistant.create_budget(income, expenses)
                        print('✅ Budget created:')
                        print(f"   Income: ${out['income']:.2f}")
                        print(f"   Expenses: ${out['expenses']:.2f}")
                        print(f"   Recommended savings: ${out['recommended_savings']:.2f}")
                        print(f"   Leftover: ${out['leftover']:.2f}")
                    except ValueError as e:
                        print(f'❌ Error: {e}')
                    continue
            print('❌ Could not parse. Try: Income 4000 Expenses 2500')
            continue

        # Log expense
        m = re.match(r'^(log(?: expense)?)\s+\$?([0-9,\.]+)\s+(.+)$', low, re.I)
        if m:
            amount = _parse_amount(m.group(2))
            category = m.group(3).strip().title()
            if amount is not None:
                try:
                    entry = assistant.log_expense(amount, category)
                    print(f"✅ Logged: ${entry.amount:.2f} in {entry.category} on {entry.date}")
                except ValueError as e:
                    print(f'❌ Error: {e}')
                continue
            print('❌ Could not parse amount.')
            continue

        # Add a single debt
        if low.startswith('add debt') or low.startswith('debt add'):
            tokens = text.split()
            if len(tokens) >= 5:
                name = tokens[2]
                balance = _parse_amount(tokens[3])
                interest = _parse_amount(tokens[4])
                minimum = _parse_amount(tokens[5]) if len(tokens) > 5 else 0.0
                if balance is not None and interest is not None:
                    try:
                        assistant.manage_debt(name, balance, interest, minimum)
                        print(f"✅ Debt '{name}' recorded: ${balance:.2f} @ {interest}% (min ${minimum:.2f})")
                    except ValueError as e:
                        print(f'❌ Error: {e}')
                    continue
            print('❌ Use: Add debt CreditCard 1500 18 50')
            continue

        # Show expense summary
        if low in ('show summary', 'expense summary', 'how much did i spend this month', 'show expenses'):
            s = assistant.expense_summary()
            print('📊 Expense summary:')
            print(f'   Total spent: ${s["total_spent"]:.2f}')
            print('   By category:')
            for k, v in s['by_category'].items():
                print(f'     - {k}: ${v:.2f}')
            continue

        # Show budget
        if low in ('show budget', 'show my budget'):
            if assistant.user_data:
                print('💵 Current budget:')
                print(f"   Income: ${assistant.user_data.get('income', 0):.2f}")
                print(f"   Expenses: ${assistant.user_data.get('expenses_total', 0):.2f}")
                print(f"   Recommended savings: ${assistant.user_data.get('recommended_savings', 0):.2f}")
            else:
                print('⚠️  No budget set. Create one with: Income <amount> Expenses <amount>')
            continue

        # Export
        if low in ('export expenses', 'export my expenses'):
            from .export import export_expenses_csv
            try:
                export_expenses_csv(assistant, 'exports/expenses.csv')
                print('✅ Exported expenses to exports/expenses.csv')
            except Exception as e:
                print(f'❌ Export failed: {e}')
            continue

        if low in ('export debts', 'export my debts'):
            from .export import export_debts_csv
            try:
                export_debts_csv(assistant, 'exports/debts.csv')
                print('✅ Exported debts to exports/debts.csv')
            except Exception as e:
                print(f'❌ Export failed: {e}')
            continue

        # Fallback to AIML
        response = kernel.respond(text)
        if response:
            # Handle ACTION: markers produced by AIML
            if response.startswith('ACTION:'):
                action = response.split(':', 1)[1].strip()
                from .parsers import parse_expense_segments, parse_debt_segments
                
                if action == 'SHOW_SUMMARY':
                    s = assistant.expense_summary()
                    print('📊 Expense summary:')
                    print(f'   Total spent: ${s["total_spent"]:.2f}')
                    print('   By category:')
                    for k, v in s['by_category'].items():
                        print(f'     - {k}: ${v:.2f}')
                    continue
                    
                if action == 'SHOW_BUDGET':
                    if assistant.user_data:
                        print('💵 Current budget:')
                        print(f"   Income: ${assistant.user_data.get('income', 0):.2f}")
                        print(f"   Expenses: ${assistant.user_data.get('expenses_total', 0):.2f}")
                        print(f"   Recommended savings: ${assistant.user_data.get('recommended_savings', 0):.2f}")
                    else:
                        print('⚠️  No budget set.')
                    continue
                    
                if action == 'SHOW_GOALS':
                    goals = assistant.savings_progress()
                    if goals:
                        print('🎯 Savings goals:')
                        for g in goals:
                            print(f'   {g}')
                    else:
                        print('⚠️  No savings goals set.')
                    continue
                    
                if action == 'EXPORT_EXPENSES':
                    from .export import export_expenses_csv
                    try:
                        export_expenses_csv(assistant, 'exports/expenses.csv')
                        print('✅ Exported to exports/expenses.csv')
                    except Exception as e:
                        print(f'❌ Export failed: {e}')
                    continue
                    
                if action == 'EXPORT_DEBTS':
                    from .export import export_debts_csv
                    try:
                        export_debts_csv(assistant, 'exports/debts.csv')
                        print('✅ Exported to exports/debts.csv')
                    except Exception as e:
                        print(f'❌ Export failed: {e}')
                    continue
                    
                if action == 'DEBT_PLAN':
                    plan = assistant.debt_payoff_plan()
                    print('📋 Debt payoff plan (avalanche method):')
                    for p in plan:
                        print(f'   {p}')
                    continue
                    
                if action == 'SUGGEST_SAVINGS':
                    income = assistant.user_data.get('income')
                    if income:
                        rec = assistant.user_data.get('recommended_savings', 0)
                        print(f'💰 Suggested savings: ${rec:.2f}')
                    else:
                        print('⚠️  Set your budget first: Income <amount> Expenses <amount>')
                    continue
                    
                if action == 'REQUEST_BUDGET':
                    print('💡 Create a budget: Income <amount> Expenses <amount>')
                    continue
                    
                if action in ('LOG_EXPENSE', 'LOG_EXPENSES', 'LOG_GENERIC'):
                    items = parse_expense_segments(text)
                    if not items:
                        print('❌ Could not parse. Try: Log 200 groceries; 50 dining')
                    else:
                        for amt, cat in items:
                            if amt is None:
                                print(f"⚠️  Skipping invalid amount for '{cat}'")
                                continue
                            try:
                                entry = assistant.log_expense(amt, cat.title())
                                print(f"✅ Logged: ${entry.amount:.2f} in {entry.category}")
                            except ValueError as e:
                                print(f'❌ Error: {e}')
                    continue
                    
                if action == 'ADD_DEBTS':
                    debts = parse_debt_segments(text)
                    if not debts:
                        print('❌ Use: Add debts CreditCard 1500 18 50; StudentLoan 10000 5 100')
                    else:
                        for name, bal, ir, mn in debts:
                            if bal is None or ir is None:
                                print(f"⚠️  Skipping invalid: {name}")
                                continue
                            try:
                                assistant.manage_debt(name, bal, ir, mn or 0.0)
                                print(f"✅ Debt '{name}': ${bal:.2f} @ {ir}% (min ${mn})")
                            except ValueError as e:
                                print(f'❌ Error: {e}')
                    continue
                    
                if action.startswith('SET_GOAL'):
                    # Parse goal name and target date from action payload
                    parts = action.split(None, 2)
                    if len(parts) >= 3:
                        try:
                            goal_name = parts[1]
                            target = parts[2]
                            # Try to extract amount from original text
                            nums = re.findall(r"[-+]?[0-9]*\.?[0-9]+", text)
                            if nums:
                                amount = float(nums[0])
                                assistant.set_savings_goal(goal_name, amount, target)
                                print(f"✅ Goal '{goal_name}' set: ${amount:.2f} by {target}")
                            else:
                                print('❌ Could not parse goal amount')
                        except ValueError as e:
                            print(f'❌ Error: {e}')
                    continue
                    
            # Otherwise print AIML response text
            print(response)
        else:
            print("❓ I didn't understand that. Type 'help' for commands.")


if __name__ == '__main__':
    run_console()
