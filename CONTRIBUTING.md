# Contributing to FinanceFlow

First off, thank you for considering contributing to FinanceFlow! It's people like you that make FinanceFlow such a great tool. 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)
- [Commit Messages](#commit-messages)

---

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python/Node version)

**Example:**
```markdown
**Bug:** Expense reset fails when database is empty

**Steps to reproduce:**
1. Fresh install with no expenses
2. Click "Reset Expenses" button
3. Error appears in console

**Expected:** Should show "0 expenses deleted" message
**Actual:** Server error 500

**Environment:** Windows 11, Python 3.11, Chrome 120
```

### 💡 Suggesting Features

Feature requests are welcome! Please provide:

- **Clear use case** - Why is this feature needed?
- **Proposed solution** - How should it work?
- **Alternatives considered** - What other approaches did you think about?
- **Mockups/examples** (if applicable)

### 🔧 Code Contributions

1. **Fork the repository**
2. **Create a feature branch** from `main`
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

---

## Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### Local Setup

1. **Clone your fork:**
```bash
git clone https://github.com/YOUR-USERNAME/financeflow.git
cd financeflow
```

2. **Set up Python environment:**
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
# or
.venv\Scripts\Activate.ps1     # Windows PowerShell
# or
source .venv/bin/activate      # Mac/Linux

pip install -r requirements.txt
pip install pytest black ruff mypy  # Dev dependencies
```

3. **Set up frontend:**
```bash
cd frontend
npm install
cd ..
```

4. **Run the app:**
```bash
# Backend (Terminal 1)
python -m uvicorn backend.main:app --reload --port 8000

# Frontend (Terminal 2)
cd frontend
npm run dev
```

5. **Verify setup:**
- Backend: http://localhost:8000/health
- Frontend: http://localhost:5173

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines (see below)
- [ ] All tests pass (`pytest`)
- [ ] New tests added for new features
- [ ] Documentation updated (README.md, docstrings)
- [ ] No linting errors (`black`, `ruff`)
- [ ] Commits are clean and descriptive

### PR Checklist

1. **Update CHANGELOG.md** with your changes
2. **Describe the changes** in PR description
3. **Link related issues** (Fixes #123)
4. **Add screenshots** for UI changes
5. **Request review** from maintainers

### PR Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix works
- [ ] New and existing tests pass locally
```

---

## Style Guidelines

### Python Code Style

We use **Black** for formatting and **Ruff** for linting.

**Before committing:**
```bash
# Format code
black src/ backend/ ml/

# Check linting
ruff check src/ backend/ ml/

# Type checking
mypy src/
```

**Key Points:**
- PEP 8 compliance
- Line length: 88 characters (Black default)
- Type hints for function signatures
- Docstrings for all public functions/classes
- Descriptive variable names

**Example:**
```python
def calculate_savings(
    income: float, 
    expenses: float, 
    savings_rate: float = 0.20
) -> dict[str, float]:
    """Calculate monthly savings based on income and expenses.
    
    Args:
        income: Monthly income in INR
        expenses: Monthly expenses in INR
        savings_rate: Target savings rate (0.0 to 1.0)
    
    Returns:
        Dictionary with savings breakdown
    """
    savings = income * savings_rate
    leftover = income - expenses - savings
    
    return {
        "savings": savings,
        "leftover": leftover,
        "savings_rate": savings_rate
    }
```

### JavaScript Code Style

**Key Points:**
- ESLint/Prettier for formatting
- Functional components with hooks
- Descriptive variable/function names
- JSDoc comments for complex functions
- Consistent file naming (PascalCase for components)

**Example:**
```javascript
/**
 * Format amount in Indian Rupee format
 * @param {number} amount - Amount to format
 * @returns {string} Formatted string (e.g., "₹12,34,567.00")
 */
export const formatCurrency = (amount) => {
  const formatted = formatIndianNumber(amount);
  return `₹${formatted}`;
};
```

### Commit Messages

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Build/config changes

**Examples:**
```bash
feat(expenses): add manual reset button with confirmation modal

- Add reset button to expenses section
- Implement confirmation modal with safety checks
- Show deleted/remaining count in success message
- Add auto-reset detection for new months

Closes #42
```

```bash
fix(api): handle empty database in reset endpoint

Previously threw 500 error when resetting empty database.
Now returns 200 with deleted_count=0.
```

```bash
docs(readme): update API documentation with reset endpoint
```

---

## Testing

### Running Tests

**Backend tests:**
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov=backend

# Specific file
pytest tests/test_assistant.py

# Verbose output
pytest -v
```

**Frontend tests:**
```bash
cd frontend
npm run test
```

### Writing Tests

**Python test example:**
```python
# tests/test_reset.py
import pytest
from src.pfa.assistant import PersonalFinanceAssistant

def test_reset_all_expenses():
    """Test resetting all expenses."""
    assistant = PersonalFinanceAssistant()
    
    # Add test expenses
    assistant.log_expense(500, "Groceries")
    assistant.log_expense(1200, "Dining")
    
    # Reset
    result = assistant.reset_expenses()
    
    # Verify
    assert result['deleted_count'] == 2
    assert result['remaining_count'] == 0
    assert len(assistant.expenses) == 0
```

### Test Coverage

Aim for **80%+** test coverage:
- All public methods tested
- Edge cases covered
- Error handling verified
- Integration tests for API endpoints

---

## Documentation

### Code Documentation

**Python:**
```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """One-line summary.
    
    Detailed description of what the function does,
    any important notes, and usage examples.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When validation fails
    """
```

**JavaScript:**
```javascript
/**
 * Component description
 * 
 * @param {Object} props - Component props
 * @param {Function} props.onSubmit - Callback function
 * @returns {JSX.Element} Rendered component
 */
export default function MyComponent({ onSubmit }) {
  // ...
}
```

### README Updates

When adding features, update:
- Feature list
- Usage examples
- API documentation
- Screenshots (if UI changed)

---

## Project Structure

```
financeflow/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── ml/               # ML models
├── src/pfa/          # Core library
├── tests/            # Test files
├── data/             # Database (gitignored)
└── docs/             # Additional documentation
```

**File naming:**
- Python: `snake_case.py`
- React components: `PascalCase.jsx`
- Utilities: `camelCase.js`
- Tests: `test_*.py`

---

## Code Review Process

### For Reviewers

- Be respectful and constructive
- Test the changes locally
- Check for edge cases
- Verify documentation
- Suggest improvements, don't demand

### For Contributors

- Respond to feedback promptly
- Be open to suggestions
- Ask questions if unclear
- Update based on review
- Mark conversations as resolved

---

## Getting Help

### Where to Ask

- **GitHub Issues** - Bug reports, feature requests
- **GitHub Discussions** - Questions, ideas, help
- **Pull Request Comments** - Specific code questions

### Response Time

- Issues: Within 2-3 days
- Pull Requests: Within 1 week
- Security issues: Within 24 hours

---

## Recognition

Contributors will be:
- Listed in CHANGELOG.md
- Credited in release notes
- Added to CONTRIBUTORS.md (coming soon)

---

## Thank You! 🙏

Your contributions make FinanceFlow better for everyone. Whether it's a bug fix, feature addition, or documentation improvement - every contribution matters!

Happy coding! 🚀

---

**Questions?** Open an issue or start a discussion on GitHub.
