import { useState, useEffect } from 'react';
import { createBudget, getBudget } from '../api';
import toast from 'react-hot-toast';
import { FaWallet, FaSave, FaLightbulb, FaRocket } from 'react-icons/fa';
import { motion } from 'framer-motion';
import confetti from 'canvas-confetti';
import { formatCurrency, formatInWords } from '../utils/currency';

export default function BudgetSection() {
  const [income, setIncome] = useState('');
  const [expenses, setExpenses] = useState('');
  const [savings, setSavings] = useState(10);
  const [currentBudget, setCurrentBudget] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadBudget();
  }, []);

  const loadBudget = async () => {
    try {
      const response = await getBudget();
      if (response.data.data) {
        setCurrentBudget(response.data.data);
        setIncome(response.data.data.income || '');
        setExpenses(response.data.data.expenses_total || '');
      }
    } catch (error) {
      console.error('Failed to load budget');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await createBudget({
        income: parseFloat(income),
        expenses: parseFloat(expenses),
        savings_percentage: savings / 100
      });

      // Confetti celebration!
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });

      toast.success('🎉 Budget saved! You\'re on your way to financial freedom!', {
        duration: 4000,
        style: {
          borderRadius: '12px',
          background: '#10b981',
          color: '#fff',
          padding: '16px',
        },
      });

      setCurrentBudget(response.data.data);
      loadBudget();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Oops! Couldn\'t save your budget. Try again?');
    } finally {
      setLoading(false);
    }
  };

  const recommendedSavings = income && expenses ? (parseFloat(income) * (savings / 100)).toFixed(2) : 0;
  const leftover = income && expenses ? (parseFloat(income) - parseFloat(expenses) - recommendedSavings).toFixed(2) : 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Helpful tip banner */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-yellow-50 to-orange-50 border-l-4 border-yellow-400 p-4 rounded-r-xl"
      >
        <div className="flex items-start">
          <FaLightbulb className="text-yellow-600 mt-1 mr-3 flex-shrink-0" />
          <div>
            <h3 className="font-semibold text-gray-800 text-sm">Pro tip:</h3>
            <p className="text-sm text-gray-600 mt-1">
              Financial experts recommend saving at least 20% of your income. Start where you can and increase gradually!
            </p>
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800 flex items-center">
            <FaRocket className="mr-3 text-primary-600" />
            Build Your Budget
          </h2>
          {currentBudget && (
            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
              ✓ Budget Active
            </span>
          )}
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                💵 Monthly Income
              </label>
              <p className="text-xs text-gray-500 mb-2">What you earn each month (after taxes)</p>
              <div className="relative group">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 text-lg font-semibold">₹</span>
                <input
                  type="number"
                  value={income}
                  onChange={(e) => setIncome(e.target.value)}
                  className="input-field pl-8 transition-all group-hover:shadow-md"
                  placeholder="5,000"
                  required
                  step="0.01"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                🏠 Monthly Expenses
              </label>
              <p className="text-xs text-gray-500 mb-2">Rent, bills, food, etc.</p>
              <div className="relative group">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 text-lg font-semibold">₹</span>
                <input
                  type="number"
                  value={expenses}
                  onChange={(e) => setExpenses(e.target.value)}
                  className="input-field pl-8 transition-all group-hover:shadow-md"
                  placeholder="3,000"
                  required
                  step="0.01"
                />
              </div>
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-semibold text-gray-700">
                💰 Savings Goal
              </label>
              <span className="text-2xl font-bold text-primary-600">{savings}%</span>
            </div>
            <p className="text-xs text-gray-500 mb-3">Slide to set your savings target</p>
            <div className="relative">
              <input
                type="range"
                min="0"
                max="50"
                value={savings}
                onChange={(e) => setSavings(parseInt(e.target.value))}
                className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer hover:h-4 transition-all"
                style={{
                  background: `linear-gradient(to right, #10b981 0%, #0ea5e9 ${savings * 2}%, #e5e7eb ${savings * 2}%, #e5e7eb 100%)`
                }}
              />
              <div className="flex justify-between text-xs text-gray-400 mt-2 font-medium">
                <span>😅 Just starting</span>
                <span>🎯 Sweet spot</span>
                <span>🚀 Ambitious!</span>
              </div>
            </div>
          </div>

          {income && expenses && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
              className="relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600 opacity-5 rounded-2xl"></div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-6 bg-white border-2 border-primary-100 rounded-2xl">
                <div className="text-center p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl border border-green-200">
                  <p className="text-xs font-medium text-gray-600 mb-2">Monthly Savings 🎯</p>
                  <p className="text-3xl font-bold text-green-600">₹{recommendedSavings}</p>
                  <p className="text-xs text-gray-500 mt-1">That's ₹{(recommendedSavings / 30).toFixed(2)}/day!</p>
                </div>
                <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl border border-blue-200">
                  <p className="text-xs font-medium text-gray-600 mb-2">After Expenses 💳</p>
                  <p className="text-3xl font-bold text-blue-600">
                    ₹{(parseFloat(income) - parseFloat(expenses)).toFixed(2)}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">Available to allocate</p>
                </div>
                <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border border-purple-200">
                  <p className="text-xs font-medium text-gray-600 mb-2">Fun Money 🎉</p>
                  <p className={`text-3xl font-bold ${leftover >= 0 ? 'text-purple-600' : 'text-red-600'}`}>
                    ₹{leftover}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {leftover >= 0 ? 'Guilt-free spending!' : 'Adjust your budget'}
                  </p>
                </div>
              </div>
            </motion.div>
          )}

          <button
            type="submit"
            disabled={loading || !income || !expenses}
            className="btn-primary w-full flex items-center justify-center space-x-2 text-lg py-4 disabled:opacity-50 disabled:cursor-not-allowed hover:scale-[1.02] active:scale-[0.98]"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <>
                <FaSave />
                <span>{currentBudget ? 'Update My Budget' : 'Lock It In!'}</span>
              </>
            )}
          </button>
        </form>
      </motion.div>
    </div>
  );
}
