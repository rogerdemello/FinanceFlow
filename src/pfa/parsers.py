"""Parsing helpers for expense and debt segments used by the AIML bot.

These functions are unit-tested in `tests/test_parsers.py`.
"""

from typing import List, Tuple, Optional
import re


def parse_expense_segments(raw_text: str) -> List[Tuple[Optional[float], str]]:
    """Parse multiple expense segments like '200 groceries; 50 dining' into (amount, category).

    Returns a list of tuples (amount or None, category string).
    """
    parts = [p.strip() for p in re.split(r";|,", raw_text) if p.strip()]
    items = []
    for p in parts:
        m = re.search(r"\$?([0-9,]*\.?[0-9]+)", p)
        if m:
            try:
                amt = float(m.group(1).replace(",", ""))
            except Exception:
                amt = None
            cat = p[m.end() :].strip()
            if not cat:
                # fallback to Misc if no category provided
                cat = "Misc"
            items.append((amt, cat))
        else:
            items.append((None, p))
    return items


def parse_debt_segments(
    raw_text: str,
) -> List[Tuple[str, Optional[float], Optional[float], Optional[float]]]:
    """Parse debts separated by semicolon: 'CreditCard 1500 18 50; Loan 10000 5 100'.

    Returns list of tuples (name, balance, interest_rate, minimum_payment).
    If a numeric field cannot be parsed, it's set to None.
    """
    segs = [s.strip() for s in re.split(r";", raw_text) if s.strip()]
    debts = []
    for s in segs:
        # remove leading command words
        s_clean = re.sub(r"(?i)^add\s+debts?\s*", "", s).strip()
        toks = s_clean.split()
        if len(toks) >= 4:
            name = toks[0]

            def _num(x):
                try:
                    return float(x.replace(",", ""))
                except Exception:
                    return None

            bal = _num(toks[1])
            ir = _num(toks[2])
            mn = _num(toks[3])
            debts.append((name, bal, ir, mn))
        else:
            nums = re.findall(r"[-+]?[0-9]*\.?[0-9]+", s_clean)
            if len(nums) >= 3:
                name = s_clean.split()[0]
                bal = float(nums[0])
                ir = float(nums[1])
                mn = float(nums[2])
                debts.append((name, bal, ir, mn))
            elif len(nums) == 2:
                name = s_clean.split()[0]
                bal = float(nums[0])
                ir = float(nums[1])
                debts.append((name, bal, ir, None))
            elif len(nums) == 1:
                name = s_clean.split()[0]
                bal = float(nums[0])
                debts.append((name, bal, None, None))
            else:
                debts.append((s_clean, None, None, None))
    return debts


__all__ = ["parse_expense_segments", "parse_debt_segments"]
