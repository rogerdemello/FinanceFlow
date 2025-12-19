import { useState, useEffect } from 'react';
import { getDashboardStats, getExpenseSummary } from '../api';
import { FaWallet, FaCreditCard, FaBullseye, FaChartPie, FaRocket, FaFire } from 'react-icons/fa';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';
import { motion } from 'framer-motion';
import { formatCurrency } from '../utils/currency';

const COLORS = ['#0ea5e9', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#ef4444'];

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [expenseSummary, setExpenseSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, summaryRes] = await Promise.all([
        getDashboardStats(),
        getExpenseSummary()
      ]);
      setStats(statsRes.data.data);
      setExpenseSummary(summaryRes.data.data);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96">
        <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p className="text-gray-500 animate-pulse">Loading your financial overview...</p>
      </div>
    );
  }

  const hasAnyData = stats?.expense_count > 0 || stats?.debt_count > 0 || stats?.goal_count > 0 || stats?.budget?.income;

  const statCards = [
    {
      title: '💸 Total Spent',
      value: `₹${stats?.total_spent?.toFixed(2) || '0.00'}`,
      icon: FaWallet,
      gradient: 'from-blue-500 to-blue-600',
      count: `${stats?.expense_count || 0} ${stats?.expense_count === 1 ? 'expense' : 'expenses'}`,
      emoji: '💰'
    },
    {
      title: '💳 Total Debt',
      value: `₹${stats?.total_debt?.toFixed(2) || '0.00'}`,
      icon: FaCreditCard,
      gradient: 'from-red-500 to-red-600',
      count: `${stats?.debt_count || 0} ${stats?.debt_count === 1 ? 'debt' : 'debts'}`,
      emoji: '🏦'
    },
    {
      title: '🎯 Savings Goals',
      value: `₹${stats?.total_goals?.toFixed(2) || '0.00'}`,
      icon: FaBullseye,
      gradient: 'from-green-500 to-green-600',
      count: `${stats?.goal_count || 0} ${stats?.goal_count === 1 ? 'goal' : 'goals'}`,
      emoji: '💎'
    },
    {
      title: '📊 Budget Status',
      value: stats?.budget?.income ? `₹${stats.budget.recommended_savings.toFixed(2)}` : 'Not Set',
      icon: FaChartPie,
      gradient: 'from-purple-500 to-purple-600',
      count: stats?.budget?.income ? 'monthly target' : 'get started!',
      emoji: stats?.budget?.income ? '✅' : '⚡'
    },
  ];

  const categoryData = expenseSummary?.by_category
    ? Object.entries(expenseSummary.by_category).map(([name, value]) => ({
        name,
        value
      }))
    : [];

  return (
    <div className="space-y-8">
      {/* Welcome message if no data */}
      {!hasAnyData && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card bg-gradient-to-br from-primary-50 via-purple-50 to-pink-50 border-2 border-primary-200"
        >
          <div className="text-center py-8">
            <div className="text-6xl mb-4">🚀</div>
            <h2 className="text-3xl font-bold text-gray-800 mb-3">Welcome to FinanceFlow!</h2>
            <p className="text-lg text-gray-600 mb-6">Let's get your finances organized and thriving</p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
              <div className="p-4 bg-white rounded-xl shadow-sm">
                <div className="text-3xl mb-2">💰</div>
                <p className="font-semibold text-gray-800">Set a Budget</p>
                <p className="text-sm text-gray-500">Know where you stand</p>
              </div>
              <div className="p-4 bg-white rounded-xl shadow-sm">
                <div className="text-3xl mb-2">📊</div>
                <p className="font-semibold text-gray-800">Track Spending</p>
                <p className="text-sm text-gray-500">See the patterns</p>
              </div>
              <div className="p-4 bg-white rounded-xl shadow-sm">
                <div className="text-3xl mb-2">🎯</div>
                <p className="font-semibold text-gray-800">Reach Goals</p>
                <p className="text-sm text-gray-500">Save for dreams</p>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.05, y: -5 }}
            className={`stat-card bg-gradient-to-br ${stat.gradient} cursor-pointer relative overflow-hidden`}
          >
            <div className="absolute top-0 right-0 text-7xl opacity-10">{stat.emoji}</div>
            <div className="flex items-center justify-between mb-4 relative z-10">
              <h3 className="text-sm font-semibold text-white/90">{stat.title}</h3>
              <stat.icon className="text-2xl text-white/90" />
            </div>
            <p className="text-4xl font-bold text-white mb-1 relative z-10">{stat.value}</p>
            <p className="text-sm text-white/80 relative z-10">{stat.count}</p>
          </motion.div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Expense Breakdown */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card"
        >
          <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
            <FaChartPie className="mr-3 text-primary-600" />
            Expenses by Category
          </h2>
          {categoryData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-400">
              <div className="text-center">
                <FaChartPie className="text-6xl mx-auto mb-4 opacity-20" />
                <p>No expense data yet</p>
              </div>
            </div>
          )}
        </motion.div>

        {/* Budget Overview */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card"
        >
          <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center">
            <FaWallet className="mr-3 text-primary-600" />
            Budget Overview
          </h2>
          {stats?.budget ? (
            <div className="space-y-4">
              <div className="p-4 bg-blue-50 rounded-xl">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Income</span>
                  <span className="text-xl font-bold text-blue-600">
                    ${stats.budget.income.toFixed(2)}
                  </span>
                </div>
              </div>
              <div className="p-4 bg-red-50 rounded-xl">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Expenses</span>
                  <span className="text-xl font-bold text-red-600">
                    ${stats.budget.expenses_total.toFixed(2)}
                  </span>
                </div>
              </div>
              <div className="p-4 bg-green-50 rounded-xl">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Recommended Savings</span>
                  <span className="text-xl font-bold text-green-600">
                    ${stats.budget.recommended_savings.toFixed(2)}
                  </span>
                </div>
              </div>
              <div className="p-4 bg-purple-50 rounded-xl border-2 border-purple-200">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Leftover</span>
                  <span className="text-2xl font-bold text-purple-600">
                    ${(stats.budget.income - stats.budget.expenses_total - stats.budget.recommended_savings).toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-400">
              <div className="text-center">
                <FaWallet className="text-6xl mx-auto mb-4 opacity-20" />
                <p>No budget configured</p>
                <p className="text-sm mt-2">Go to Budget tab to create one</p>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
