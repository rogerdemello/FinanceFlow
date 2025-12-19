# Changelog

All notable changes to FinanceFlow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-12-19

### 🎉 Major Release - Production Ready

Complete rewrite with modern web UI, AI/ML features, and Indian market optimization.

### Added

#### Web UI
- ✨ Beautiful React-based web interface with Vite
- 🎨 Tailwind CSS with custom gradient design system
- 📊 Interactive charts using Recharts (Pie, Bar charts)
- ✨ Smooth animations with Framer Motion
- 🔔 Toast notifications with React Hot Toast
- 📱 Fully responsive design (mobile, tablet, desktop)
- 🎉 Confetti celebrations for budget saves and goal completions

#### AI/ML Features
- 🤖 Machine learning expense categorizer (scikit-learn)
  - TF-IDF vectorization for text features
  - Naive Bayes classifier
  - 90%+ accuracy on Indian spending patterns
  - Confidence scoring for predictions
- 🗣️ Natural language processing for expense entry
  - Parse "spent 500 on groceries yesterday"
  - Extract amount, category, merchant, date, payment method
  - Support for relative dates (yesterday, last week)
  - Indian merchant recognition (Swiggy, Zomato, DMart, etc.)
- 💡 Real-time category suggestions as you type
- 🇮🇳 12 expense categories optimized for India
- 📊 AI confidence display for transparency

#### Indian Market Features
- 💰 Complete INR (₹) currency support throughout
- 🇮🇳 Indian number formatting utilities (lakhs/crores ready)
- 🏪 Recognition of 25+ Indian merchants and brands
  - Food: Swiggy, Zomato
  - Retail: DMart, BigBazaar, Flipkart, Amazon, Myntra
  - Transport: Uber, Ola
  - Healthcare: Apollo, Medlife
  - Entertainment: Netflix, Hotstar, BookMyShow
  - Finance: Paytm, GPay, PhonePe, Zerodha, Groww
- 💳 UPI payment method support
- 🏷️ India-specific expense categories

#### Smart Features
- 🔄 Auto-reset prompts at start of each month
- 🗑️ Manual expense reset with confirmation modal
- 💾 Enhanced SQLite persistence
- 📤 CSV export/import for expenses and debts
- ⚡ Real-time UI updates
- 🎯 Empty states with helpful guidance
- 💬 Conversational UI copy

#### Components
- 📊 Dashboard with live stats and welcome screen
- 💰 Budget planner with visual feedback
- 💸 Expenses tracker with AI entry
- 💳 Debt manager with payoff strategies
- 🎯 Goals tracker with progress monitoring
- 🤖 NLP expense entry component (purple gradient AI card)

#### API Endpoints
- `POST /api/expenses/nlp` - Natural language expense creation
- `GET /api/expenses/suggest-category` - AI category suggestions
- `DELETE /api/expenses/reset` - Reset expenses (full or date-based)
- `GET /health` - Health check with ML status
- `GET /api/ai/status` - AI features availability

### Changed
- 🎨 Complete UI redesign - modern, gradient-based
- 🏢 Renamed app to "FinanceFlow"
- 💬 Better UX copy throughout ("Fun Money" vs "Leftover")
- 📊 Enhanced dashboard with dual metrics
- 🎭 Improved empty states with emojis and guidance
- ⚡ Better loading states and error handling
- 🔔 Rich toast notifications with gradient backgrounds

### Fixed
- 🐛 Daily savings calculation (was /12, now /30)
- 🔢 Number formatting consistency
- 🎯 Form validation edge cases
- 💾 Database persistence reliability
- 🔄 Real-time data refresh issues

### Technical
- ⚡ FastAPI backend (Python 3.9+)
- ⚛️ React 18 frontend
- 🎨 Tailwind CSS styling
- 📊 Recharts for visualizations
- 🤖 scikit-learn for ML
- 💾 SQLite database
- 🧪 Pytest for testing
- 📦 Vite for frontend builds

---

## [1.0.0] - 2024-12-01

### Initial Release - CLI Version

#### Added
- ✅ Core PersonalFinanceAssistant class
- ✅ Budget creation and management
- ✅ Expense tracking with categories
- ✅ Debt management (Avalanche/Snowball strategies)
- ✅ Savings goals setting
- ✅ SQLite persistence
- ✅ CSV export for expenses and debts
- ✅ Input validation
- ✅ CLI demo script
- ✅ AIML conversational interface
- ✅ Basic test suite
- ✅ Pre-commit hooks
- ✅ CI/CD setup

#### Technical
- Python 3.9+ support
- AIML for conversational AI
- TextBlob for sentiment analysis
- Pytest for testing
- Black for code formatting
- Ruff for linting

---

## [Unreleased]

### Planned for 2.1
- [ ] User authentication (JWT)
- [ ] PostgreSQL support
- [ ] Receipt OCR scanning
- [ ] Email notifications
- [ ] Export to PDF
- [ ] Recurring expenses
- [ ] Bill reminders

### Planned for 3.0
- [ ] Financial chatbot (LLM integration)
- [ ] Multi-currency support
- [ ] Mobile app (React Native)
- [ ] Investment tracking
- [ ] Advanced analytics

### Planned for 4.0
- [ ] Multi-user support
- [ ] Collaboration features
- [ ] Tax calculation
- [ ] Bank integration (Plaid/Yodlee)

---

## Version History

- **2.0.0** (2025-12-19) - Production ready with web UI and AI
- **1.0.0** (2024-12-01) - Initial CLI version

---

## Migration Guide

### From 1.0 to 2.0

**Breaking Changes:**
- CLI interface deprecated (still available but not recommended)
- Database schema unchanged (fully compatible)
- New web UI as primary interface

**Upgrade Steps:**
1. Pull latest code: `git pull origin main`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```
3. Start web UI: `./start-ui.sh` or `start-ui.bat`
4. Your existing SQLite data will work automatically!

**New Features to Try:**
1. AI Natural Language Entry - type "spent 500 on groceries"
2. Auto-reset prompts at month start
3. Confetti celebrations 🎉
4. Beautiful gradient UI

---

## Contributors

- [@rogerdemello] - Original author and maintainer

---

## Links

- [Repository](https://github.com/rogerdemello/FinanceFlow)
- [Issue Tracker](https://github.com/rogerdemello/FinanceFlow/issues)

---

**Contributions are most welcome to make FinanceFlow better!**
