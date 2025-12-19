"""FastAPI backend for Personal Finance Assistant with AI/ML features."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pfa.assistant import PersonalFinanceAssistant
from src.pfa.export import export_expenses_csv, export_debts_csv

# Import ML modules
ml_path = Path(__file__).parent.parent / "ml"
sys.path.insert(0, str(ml_path))

try:
    from expense_categorizer import ExpenseCategorizer
    from nlp_expense_parser import NLPExpenseParser
    ML_ENABLED = True
except ImportError:
    ML_ENABLED = False
    print("⚠️  Warning: ML modules not found. AI features disabled.")

app = FastAPI(
    title="Personal Finance Assistant API - India Edition",
    description="AI-powered personal finance management 🇮🇳",
    version="2.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize assistant with persistence
assistant = PersonalFinanceAssistant(db_path="data/db.sqlite3")

# Initialize AI/ML components
if ML_ENABLED:
    expense_categorizer = ExpenseCategorizer()
    nlp_parser = NLPExpenseParser()
    print("✅ AI features enabled: Smart categorization & NLP expense entry")
else:
    expense_categorizer = None
    nlp_parser = None


# Pydantic models
class BudgetCreate(BaseModel):
    income: float = Field(gt=0, description="Monthly income")
    expenses: float = Field(ge=0, description="Monthly expenses")
    savings_percentage: float = Field(default=0.10, ge=0, le=1)


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)


class DebtCreate(BaseModel):
    name: str = Field(min_length=1)
    balance: float = Field(ge=0)
    interest_rate: float = Field(ge=0)
    minimum_payment: float = Field(ge=0)


class SavingsGoalCreate(BaseModel):
    goal_name: str = Field(min_length=1)
    target_amount: float = Field(gt=0)
    target_date: str


class NLPExpenseCreate(BaseModel):
    """Natural language expense input for AI parsing"""
    text: str = Field(..., description="e.g., 'spent 500 on groceries yesterday'")


# ===== Health & AI Status =====

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ml_enabled": ML_ENABLED,
        "currency": "INR",
        "region": "India"
    }


@app.get("/api/ai/status")
async def get_ai_status():
    """Check AI/ML features availability"""
    return {
        "status": "success",
        "data": {
            "ml_enabled": ML_ENABLED,
            "features": {
                "smart_categorization": ML_ENABLED,
                "nlp_expense_entry": ML_ENABLED,
                "auto_suggestions": ML_ENABLED
            }
        }
    }
    name: str = Field(min_length=1)
    amount: float = Field(gt=0)
    target_date: str


# Budget endpoints
@app.post("/api/budget")
async def create_budget(budget: BudgetCreate):
    """Create or update budget."""
    try:
        result = assistant.create_budget(
            budget.income, budget.expenses, budget.savings_percentage
        )
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/budget")
async def get_budget():
    """Get current budget."""
    return {
        "success": True,
        "data": assistant.user_data if assistant.user_data else None,
    }


# Expense endpoints
@app.post("/api/expenses")
async def create_expense(expense: ExpenseCreate):
    """Log a new expense."""
    try:
        entry = assistant.log_expense(expense.amount, expense.category)
        return {
            "success": True,
            "data": {
                "amount": entry.amount,
                "category": entry.category,
                "date": entry.date,
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/expenses")
async def get_expenses():
    """Get all expenses."""
    expenses = [
        {"amount": e.amount, "category": e.category, "date": e.date}
        for e in assistant.expenses
    ]
    return {"success": True, "data": expenses}


# AI-Powered Expense Endpoints
@app.post("/api/expenses/nlp")
async def create_expense_nlp(request: NLPExpenseCreate):
    """
    Add expense using natural language (AI-powered)
    
    Example: "spent 500 on groceries yesterday"
    """
    if not ML_ENABLED:
        raise HTTPException(
            status_code=503,
            detail="AI features not available. Please use the standard form."
        )
    
    try:
        # Parse natural language input
        parsed = nlp_parser.parse(request.text)
        
        if not nlp_parser.validate(parsed):
            raise HTTPException(
                status_code=400,
                detail="Could not understand. Try: 'spent [amount] on [category]'"
            )
        
        # Log expense
        entry = assistant.log_expense(parsed['amount'], parsed['category'])
        
        return {
            "success": True,
            "data": {
                "amount": entry.amount,
                "category": entry.category,
                "date": entry.date,
                "auto_categorized": True,
                "confidence": parsed.get('confidence', 0),
                "merchant": parsed.get('merchant'),
            },
            "ai_insights": {
                "parsed_text": request.text,
                "confidence": parsed.get('confidence', 0),
                "detected_category": parsed['category'],
                "detected_merchant": parsed.get('merchant')
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/expenses/suggest-category")
async def suggest_category(description: str):
    """
    Get AI-powered category suggestion based on description
    
    Example: /api/expenses/suggest-category?description=swiggy dinner
    """
    if not ML_ENABLED:
        raise HTTPException(status_code=503, detail="AI features not available")
    
    try:
        category, confidence = expense_categorizer.predict(description)
        
        return {
            "success": True,
            "data": {
                "suggested_category": category,
                "confidence": round(confidence, 2),
                "description": f"{confidence:.0%} confident this is {category}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/expenses/summary")
async def get_expense_summary():
    """Get expense summary with totals by category."""
    summary = assistant.expense_summary()
    return {"success": True, "data": summary}


@app.delete("/api/expenses/reset")
async def reset_expenses(before_date: Optional[str] = None):
    """Reset (delete) all expenses or expenses before a specific date.
    
    Query params:
        before_date: Optional YYYY-MM-DD format. If provided, deletes expenses before this date.
                    If omitted, deletes all expenses.
    
    Example:
        DELETE /api/expenses/reset  (delete all)
        DELETE /api/expenses/reset?before_date=2024-01-01  (delete before date)
    """
    try:
        result = assistant.reset_expenses(before_date)
        return {
            "success": True,
            "data": result,
            "message": f"Deleted {result['deleted_count']} expense(s). {result['remaining_count']} remaining."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Debt endpoints
@app.post("/api/debts")
async def create_debt(debt: DebtCreate):
    """Add or update a debt."""
    try:
        result = assistant.manage_debt(
            debt.name, debt.balance, debt.interest_rate, debt.minimum_payment
        )
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/debts")
async def get_debts():
    """Get all debts."""
    debts = [
        {
            "name": name,
            "balance": info["balance"],
            "interest_rate": info["interest_rate"],
            "minimum_payment": info["minimum_payment"],
        }
        for name, info in assistant.debt.items()
    ]
    return {"success": True, "data": debts}


@app.get("/api/debts/payoff-plan")
async def get_payoff_plan(method: str = "avalanche"):
    """Get debt payoff plan."""
    plan = assistant.debt_payoff_plan(method)
    return {"success": True, "data": plan}


# Savings goals endpoints
@app.post("/api/goals")
async def create_goal(goal: SavingsGoalCreate):
    """Create a savings goal."""
    try:
        result = assistant.set_savings_goal(goal.name, goal.amount, goal.target_date)
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/goals")
async def get_goals():
    """Get all savings goals."""
    goals = [
        {"name": name, "amount": info["amount"], "target_date": info["target_date"]}
        for name, info in assistant.savings_goals.items()
    ]
    return {"success": True, "data": goals}


# Dashboard stats
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics."""
    summary = assistant.expense_summary()
    total_debt = sum(d["balance"] for d in assistant.debt.values())
    total_goals = sum(g["amount"] for g in assistant.savings_goals.values())

    return {
        "success": True,
        "data": {
            "total_spent": summary["total_spent"],
            "expense_count": summary["count"],
            "total_debt": total_debt,
            "debt_count": len(assistant.debt),
            "total_goals": total_goals,
            "goal_count": len(assistant.savings_goals),
            "budget": assistant.user_data if assistant.user_data else None,
        },
    }


@app.get("/")
async def root():
    """API health check."""
    return {"status": "ok", "message": "Personal Finance Assistant API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
