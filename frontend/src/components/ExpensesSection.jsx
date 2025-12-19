import { useState, useEffect } from 'react';
import { createExpense, getExpenses, getExpenseSummary, resetExpenses } from '../api';
import toast from 'react-hot-toast';
import { FaPlus, FaShoppingCart, FaUtensils, FaCar, FaHome, FaEllipsisH, FaFilm, FaHeartbeat, FaTshirt, FaSmile, FaTrash, FaSync } from 'react-icons/fa';
import { motion } from 'framer-motion';
import confetti from 'canvas-confetti';
import { formatCurrency } from '../utils/currency';
import NLPExpenseEntry from './NLPExpenseEntry';

const CATEGORY_ICONS = {
  'Groceries': FaShoppingCart,
  'Dining': FaUtensils,
  'Transport': FaCar,
  'Housing': FaHome,
  'Entertainment': FaFilm,
  'Healthcare': FaHeartbeat,
  'Shopping': FaTshirt,
  'Other': FaEllipsisH
};

export default function ExpensesSection() {
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('Groceries');
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showResetModal, setShowResetModal] = useState(false);
  const [resetLoading, setResetLoading] = useState(false);

  useEffect(() => {
    loadExpenses();
    checkAutoReset();
  }, []);

  const checkAutoReset = () => {
    const lastReset = localStorage.getItem('lastExpenseReset');
    const now = new Date();
    const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    
    if (lastReset !== currentMonth && expenses.length > 0) {
      // Show notification that auto-reset is available
      const firstDayOfMonth = `${currentMonth}-01`;
      toast(
        (t) => (
          <div className="flex flex-col gap-2">
            <div className="font-semibold">🗓️ New month detected!</div>
            <div className="text-sm">Would you like to reset last month's expenses?</div>
            <div className="flex gap-2 mt-2">
              <button
                onClick={() => {
                  handleAutoReset(firstDayOfMonth);
                  toast.dismiss(t.id);
                }}
                className="px-3 py-1 bg-blue-500 text-white rounded-lg text-sm font-medium hover:bg-blue-600"
              >
                Yes, Reset
              </button>
              <button
                onClick={() => {
                  localStorage.setItem('lastExpenseReset', currentMonth);
                  toast.dismiss(t.id);
                }}
                className="px-3 py-1 bg-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-400"
              >
                Keep Them
              </button>
            </div>
          </div>
        ),
        {
          duration: 10000,
          position: 'top-center',
        }
      );
    }
  };

  const handleAutoReset = async (beforeDate) => {
    try {
      const response = await resetExpenses(beforeDate);
      const { deleted_count, remaining_count } = response.data.data;
      
      const now = new Date();
      const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
      localStorage.setItem('lastExpenseReset', currentMonth);
      
      toast.success(`✅ Deleted ${deleted_count} old expense(s). ${remaining_count} current expense(s) remain.`, {
        duration: 4000,
      });
      
      loadExpenses();
    } catch (error) {
      toast.error('Failed to auto-reset expenses');
    }
  };

  const loadExpenses = async () => {
    try {
      const [expensesRes, summaryRes] = await Promise.all([
        getExpenses(),
        getExpenseSummary()
      ]);
      setExpenses(expensesRes.data.data);
      setSummary(summaryRes.data.data);
    } catch (error) {
      console.error('Failed to load expenses');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await createExpense({
        amount: parseFloat(amount),
        category
      });

      toast.success(`✅ Tracked ₹${amount} for ${category}`, {
        duration: 3000,
        style: { 
          borderRadius: '12px',
          background: '#10b981',
          color: '#fff',
        },
      });

      setAmount('');
      loadExpenses();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Couldn\'t add that expense. Try again?');
    } finally {
      setLoading(false);
    }
  };

  const handleResetExpenses = async () => {
    setResetLoading(true);
    try {
      const response = await resetExpenses();
      const { deleted_count } = response.data.data;
      
      setShowResetModal(false);
      toast.success(`🗑️ Deleted all ${deleted_count} expense(s). Fresh start!`, {
        duration: 3000,
        style: {
          borderRadius: '12px',
          background: '#ef4444',
          color: '#fff',
        },
      });
      
      loadExpenses();
    } catch (error) {
      toast.error('Failed to reset expenses');
    } finally {
      setResetLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* AI-Powered NLP Entry */}
      <NLPExpenseEntry onExpenseAdded={loadExpenses} />

      {/* Traditional Add Expense Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card bg-gradient-to-br from-white to-blue-50/30"
      >
        <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center">
          <FaSmile className="mr-3 text-primary-600" />
          Track an Expense
        </h2>
        <p className="text-sm text-gray-500 mb-6">Keep tabs on where your money goes</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-1">
              <label className="block text-sm font-semibold text-gray-700 mb-2">💵 How much?</label>
              <div className="relative group">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 text-lg font-semibold">₹</span>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="input-field pl-8 text-lg group-hover:shadow-md transition-shadow"
                  placeholder="25.00"
                  required
                  step="0.01"
                  autoFocus
                />
              </div>
            </div>

            <div className="md:col-span-1">
              <label className="block text-sm font-semibold text-gray-700 mb-2">🏷️ What for?</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="input-field text-lg hover:shadow-md transition-shadow"
              >
                <option value="Groceries">🛒 Groceries</option>
                <option value="Dining">🍽️ Dining</option>
                <option value="Transport">🚗 Transport</option>
                <option value="Housing">🏠 Housing</option>
                <option value="Entertainment">🎬 Entertainment</option>
                <option value="Healthcare">⚕️ Healthcare</option>
                <option value="Shopping">👕 Shopping</option>
                <option value="Other">📌 Other</option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                type="submit"
                disabled={loading || !amount}
                className="btn-primary w-full flex items-center justify-center space-x-2 hover:scale-105 active:scale-95 transition-transform disabled:opacity-50"
              >
                <FaPlus />
                <span>{loading ? 'Tracking...' : 'Track It'}</span>
              </button>
            </div>
          </div>
        </form>
      </motion.div>

      {/* Summary Cards */}
      {summary && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold text-gray-700">📊 Your Spending Summary</h3>
            {expenses.length > 0 && (
              <button
                onClick={() => setShowResetModal(true)}
                className="flex items-center gap-2 px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg font-medium transition-colors border border-red-200"
              >
                <FaTrash className="text-sm" />
                <span>Reset Expenses</span>
              </button>
            )}
          </div>
          
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            <motion.div 
              whileHover={{ scale: 1.02 }}
              className="card bg-gradient-to-br from-blue-500 to-blue-600 text-white cursor-pointer"
            >
              <div className="flex justify-between items-start mb-2">
                <p className="text-sm opacity-90">💸 Total Spent</p>
                <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
              </div>
              <p className="text-4xl font-bold mb-1">₹{summary.total_spent.toFixed(2)}</p>
              <p className="text-xs opacity-75">This month</p>
            </motion.div>
            <motion.div 
              whileHover={{ scale: 1.02 }}
              className="card bg-gradient-to-br from-purple-500 to-purple-600 text-white cursor-pointer"
            >
              <p className="text-sm opacity-90 mb-2">📝 Transactions</p>
              <p className="text-4xl font-bold mb-1">{summary.count}</p>
              <p className="text-xs opacity-75">Logged expenses</p>
            </motion.div>
            <motion.div 
              whileHover={{ scale: 1.02 }}
              className="card bg-gradient-to-br from-green-500 to-green-600 text-white cursor-pointer"
            >
              <p className="text-sm opacity-90 mb-2">🏷️ Categories</p>
              <p className="text-4xl font-bold mb-1">{Object.keys(summary.by_category).length}</p>
              <p className="text-xs opacity-75">Different types</p>
            </motion.div>
          </motion.div>
        </div>
      )}

      {/* Recent Expenses */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="card"
      >
        <h2 className="text-xl font-bold text-gray-800 mb-6">📊 Recent Activity</h2>
        
        {expenses.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FaSmile className="text-4xl text-gray-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-700 mb-2">No expenses yet!</h3>
            <p className="text-gray-500">Start tracking your spending above</p>
          </div>
        ) : (
          <div className="space-y-3">
            {expenses.slice(-10).reverse().map((expense, index) => {
              const Icon = CATEGORY_ICONS[expense.category] || FaEllipsisH;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ scale: 1.01, x: 4 }}
                  className="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-white rounded-xl hover:shadow-md transition-all border border-gray-100 cursor-pointer"
                >
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-sm">
                      <Icon className="text-white text-xl" />
                    </div>
                    <div>
                      <p className="font-semibold text-gray-800">{expense.category}</p>
                      <p className="text-sm text-gray-500">{expense.date}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-xl font-bold text-gray-800">-₹{expense.amount.toFixed(2)}</p>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </motion.div>

      {/* Reset Confirmation Modal */}
      {showResetModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6"
          >
            <div className="flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mx-auto mb-4">
              <FaTrash className="text-3xl text-red-600" />
            </div>
            
            <h3 className="text-2xl font-bold text-gray-800 text-center mb-2">
              Reset All Expenses?
            </h3>
            
            <p className="text-gray-600 text-center mb-6">
              This will permanently delete all <strong>{expenses.length} expense(s)</strong>. This action cannot be undone.
            </p>
            
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-6">
              <p className="text-sm text-yellow-800">
                💡 <strong>Tip:</strong> Expenses are automatically suggested for reset at the beginning of each month!
              </p>
            </div>
            
            <div className="flex gap-3">
              <button
                onClick={() => setShowResetModal(false)}
                className="flex-1 px-4 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl font-medium transition-colors"
                disabled={resetLoading}
              >
                Cancel
              </button>
              <button
                onClick={handleResetExpenses}
                className="flex-1 px-4 py-3 bg-red-600 hover:bg-red-700 text-white rounded-xl font-medium transition-colors flex items-center justify-center gap-2"
                disabled={resetLoading}
              >
                {resetLoading ? (
                  <>
                    <FaSync className="animate-spin" />
                    <span>Resetting...</span>
                  </>
                ) : (
                  <>
                    <FaTrash />
                    <span>Yes, Reset All</span>
                  </>
                )}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
}
