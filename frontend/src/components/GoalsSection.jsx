import { useState, useEffect } from 'react';
import { createGoal, getGoals } from '../api';
import toast from 'react-hot-toast';
import { FaBullseye, FaCalendar, FaTrophy } from 'react-icons/fa';
import { motion } from 'framer-motion';
import confetti from 'canvas-confetti';

export default function GoalsSection() {
  const [name, setName] = useState('');
  const [amount, setAmount] = useState('');
  const [targetDate, setTargetDate] = useState('');
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadGoals();
  }, []);

  const loadGoals = async () => {
    try {
      const response = await getGoals();
      setGoals(response.data.data);
    } catch (error) {
      console.error('Failed to load goals');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await createGoal({
        name,
        amount: parseFloat(amount),
        target_date: targetDate
      });

      toast.success(`Goal "${name}" created!`, {
        icon: '🎯',
        style: { borderRadius: '12px' },
      });

      setName('');
      setAmount('');
      setTargetDate('');
      loadGoals();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create goal');
    } finally {
      setLoading(false);
    }
  };

  const totalGoals = goals.reduce((sum, goal) => sum + goal.amount, 0);

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Add Goal Form */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <h2 className="text-2xl font-bold text-gray-800 mb-2 flex items-center">
          <FaTrophy className="mr-3 text-yellow-500" />
          Set a Savings Goal
        </h2>
        <p className="text-sm text-gray-500 mb-6">Dream big, save smart 🚀</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Goal Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="input-field"
                placeholder="Emergency Fund"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Target Amount</label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">₹</span>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="input-field pl-8"
                  placeholder="50000"
                  required
                  step="0.01"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Target Date</label>
              <input
                type="date"
                value={targetDate}
                onChange={(e) => setTargetDate(e.target.value)}
                className="input-field"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full"
          >
            {loading ? 'Creating...' : 'Create Goal'}
          </button>
        </form>
      </motion.div>

      {/* Total Goals */}
      {goals.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="card bg-gradient-to-br from-green-500 to-green-600 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm opacity-80 mb-2">Total Savings Goals</p>
              <p className="text-5xl font-bold">₹{totalGoals.toFixed(2)}</p>
              <p className="text-sm opacity-80 mt-2">{goals.length} active goals</p>
            </div>
            <FaBullseye className="text-8xl opacity-20" />
          </div>
        </motion.div>
      )}

      {/* Goals List */}
      {goals.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h2 className="text-xl font-bold text-gray-800 mb-6">Your Goals</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {goals.map((goal, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className="p-6 bg-gradient-to-br from-green-50 via-blue-50 to-purple-50 rounded-2xl border-2 border-green-200 hover:border-green-400 transition-all"
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="font-bold text-gray-800 text-xl mb-2">{goal.name}</h3>
                    <div className="flex items-center text-sm text-gray-600">
                      <FaCalendar className="mr-2" />
                      Target: {new Date(goal.target_date).toLocaleDateString()}
                    </div>
                  </div>
                  <div className="w-14 h-14 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center shadow-lg">
                    <FaBullseye className="text-white text-2xl" />
                  </div>
                </div>

                <div className="mt-4">
                  <div className="flex justify-between items-end mb-2">
                    <span className="text-sm text-gray-600">Target Amount</span>
                    <span className="text-3xl font-bold text-green-600">
                      ₹{goal.amount.toFixed(2)}
                    </span>
                  </div>
                  
                  {/* Progress placeholder */}
                  <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-green-500 to-green-600 rounded-full transition-all duration-500"
                      style={{ width: '0%' }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">Start saving to track progress</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {goals.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="card text-center py-12"
        >
          <FaBullseye className="text-6xl text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500 text-lg">No savings goals yet</p>
          <p className="text-gray-400 text-sm mt-2">Create your first goal above to start saving!</p>
        </motion.div>
      )}
    </div>
  );
}
