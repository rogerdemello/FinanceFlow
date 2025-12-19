import { useState, useEffect } from 'react';
import { createDebt, getDebts, getPayoffPlan } from '../api';
import toast from 'react-hot-toast';
import { FaCreditCard, FaChartLine, FaFire, FaSnowflake } from 'react-icons/fa';
import { motion } from 'framer-motion';
import confetti from 'canvas-confetti';

export default function DebtsSection() {
  const [name, setName] = useState('');
  const [balance, setBalance] = useState('');
  const [interestRate, setInterestRate] = useState('');
  const [minimumPayment, setMinimumPayment] = useState('');
  const [debts, setDebts] = useState([]);
  const [payoffPlan, setPayoffPlan] = useState([]);
  const [method, setMethod] = useState('avalanche');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDebts();
  }, [method]);

  const loadDebts = async () => {
    try {
      const [debtsRes, planRes] = await Promise.all([
        getDebts(),
        getPayoffPlan(method)
      ]);
      setDebts(debtsRes.data.data);
      setPayoffPlan(planRes.data.data);
    } catch (error) {
      console.error('Failed to load debts');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await createDebt({
        name,
        balance: parseFloat(balance),
        interest_rate: parseFloat(interestRate),
        minimum_payment: parseFloat(minimumPayment)
      });

      toast.success(`✅ Debt tracked: ${name}`, {
        duration: 3000,
        style: { 
          borderRadius: '12px',
          background: '#10b981',
          color: '#fff',
        },
      });

      setName('');
      setBalance('');
      setInterestRate('');
      setMinimumPayment('');
      loadDebts();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to add debt');
    } finally {
      setLoading(false);
    }
  };

  const totalDebt = debts.reduce((sum, debt) => sum + debt.balance, 0);

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Add Debt Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center">
          <FaCreditCard className="mr-3 text-red-600" />
          Track a Debt
        </h2>
        <p className="text-sm text-gray-500 mb-6">Let's build a payoff plan 💪</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="input-field"
                placeholder="Credit Card"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Balance</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">₹</span>
                <input
                  type="number"
                  value={balance}
                  onChange={(e) => setBalance(e.target.value)}
                  className="input-field pl-8"
                  placeholder="1500"
                  required
                  step="0.01"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Interest Rate</label>
              <div className="relative">
                <input
                  type="number"
                  value={interestRate}
                  onChange={(e) => setInterestRate(e.target.value)}
                  className="input-field pr-8"
                  placeholder="18"
                  required
                  step="0.01"
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">%</span>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Min. Payment</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">₹</span>
                <input
                  type="number"
                  value={minimumPayment}
                  onChange={(e) => setMinimumPayment(e.target.value)}
                  className="input-field pl-8"
                  placeholder="500"
                  required
                  step="0.01"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full"
          >
            {loading ? 'Adding...' : 'Add Debt'}
          </button>
        </form>
      </motion.div>

      {/* Total Debt */}
      {debts.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="card bg-gradient-to-br from-red-500 to-red-600 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm opacity-80 mb-2">Total Debt</p>
              <p className="text-5xl font-bold">₹{totalDebt.toFixed(2)}</p>
              <p className="text-sm opacity-80 mt-2">{debts.length} debts to pay off</p>
            </div>
            <FaCreditCard className="text-8xl opacity-20" />
          </div>
        </motion.div>
      )}

      {/* Payoff Plan */}
      {debts.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-800 flex items-center">
              <FaChartLine className="mr-3 text-primary-600" />
              Payoff Strategy
            </h2>
            <div className="flex space-x-2">
              <button
                onClick={() => setMethod('avalanche')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  method === 'avalanche'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Avalanche
              </button>
              <button
                onClick={() => setMethod('snowball')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  method === 'snowball'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Snowball
              </button>
            </div>
          </div>

          <div className="space-y-3">
            {payoffPlan.map((plan, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border-l-4 border-primary-600"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold">
                      {index + 1}
                    </div>
                    <p className="font-medium text-gray-800">{plan}</p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Debt List */}
      {debts.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h2 className="text-xl font-bold text-gray-800 mb-6">All Debts</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {debts.map((debt, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className="p-5 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border border-gray-200"
              >
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-bold text-gray-800 text-lg">{debt.name}</h3>
                  <span className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-medium">
                    {debt.interest_rate}%
                  </span>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Balance:</span>
                    <span className="font-bold text-gray-800">₹{debt.balance.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Min. Payment:</span>
                    <span className="font-medium text-gray-700">₹{debt.minimum_payment.toFixed(2)}/mo</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
