import { useState } from 'react';
import { FaRobot, FaMagic, FaLightbulb } from 'react-icons/fa';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export default function NLPExpenseEntry({ onExpenseAdded }) {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestion, setSuggestion] = useState(null);

  const examples = [
    "spent ₹500 on groceries yesterday",
    "paid ₹1200 for Swiggy dinner",
    "uber ride ₹250 to airport",
    "bought medicine ₹450",
    "netflix subscription ₹199"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/expenses/nlp`, {
        text: text
      });

      if (response.data.success) {
        const { amount, category, confidence, merchant } = response.data.data;
        
        toast.success(
          <div>
            <div className="font-bold">✨ Expense Tracked!</div>
            <div className="text-sm">₹{amount} • {category} {merchant ? `• ${merchant}` : ''}</div>
            <div className="text-xs opacity-75">AI Confidence: {(confidence * 100).toFixed(0)}%</div>
          </div>,
          {
            duration: 4000,
            style: {
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: '#fff',
              padding: '16px',
            }
          }
        );

        setText('');
        setSuggestion(null);
        if (onExpenseAdded) onExpenseAdded();
      }
    } catch (error) {
      if (error.response?.status === 503) {
        toast.error('AI features are not available. Please install ML dependencies.');
      } else {
        toast.error(error.response?.data?.detail || 'Could not understand. Try a clearer description.');
      }
    } finally {
      setLoading(false);
    }
  };

  const getSuggestion = async (description) => {
    if (description.length < 3) {
      setSuggestion(null);
      return;
    }

    try {
      const response = await axios.get(`${API_URL}/expenses/suggest-category`, {
        params: { description }
      });

      if (response.data.success) {
        setSuggestion(response.data.data);
      }
    } catch (error) {
      setSuggestion(null);
    }
  };

  const handleTextChange = (e) => {
    const value = e.target.value;
    setText(value);
    
    // Debounced suggestion
    if (value.length >= 5) {
      const timer = setTimeout(() => getSuggestion(value), 500);
      return () => clearTimeout(timer);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card bg-gradient-to-br from-purple-50 via-blue-50 to-cyan-50 border-2 border-purple-200"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center">
            <FaRobot className="text-white text-2xl" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-800">AI Quick Entry</h3>
            <p className="text-sm text-gray-600">Just type naturally ✨</p>
          </div>
        </div>
        <div className="px-3 py-1 bg-purple-600 text-white rounded-full text-xs font-bold">
          BETA
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <div className="relative">
            <FaMagic className="absolute left-4 top-4 text-purple-400" />
            <input
              type="text"
              value={text}
              onChange={handleTextChange}
              className="w-full pl-12 pr-4 py-4 rounded-xl border-2 border-purple-300 focus:border-purple-600 focus:ring-2 focus:ring-purple-200 transition-all text-lg"
              placeholder="spent 500 on groceries yesterday..."
              required
            />
          </div>

          {/* AI Suggestion */}
          <AnimatePresence>
            {suggestion && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mt-2 p-3 bg-white rounded-lg border border-purple-200 flex items-center justify-between"
              >
                <div className="flex items-center space-x-2">
                  <FaLightbulb className="text-yellow-500" />
                  <span className="text-sm text-gray-700">
                    AI suggests: <strong className="text-purple-600">{suggestion.suggested_category}</strong>
                  </span>
                </div>
                <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                  {suggestion.confidence * 100}% sure
                </span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <button
          type="submit"
          disabled={loading || !text}
          className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 rounded-xl font-semibold hover:from-purple-700 hover:to-blue-700 transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {loading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <>
              <FaRobot />
              <span>Let AI Parse It</span>
            </>
          )}
        </button>
      </form>

      {/* Examples */}
      <div className="mt-6 pt-6 border-t border-purple-200">
        <p className="text-sm font-semibold text-gray-700 mb-3">💡 Try these examples:</p>
        <div className="space-y-2">
          {examples.map((example, index) => (
            <button
              key={index}
              onClick={() => setText(example)}
              className="block w-full text-left px-4 py-2 bg-white hover:bg-purple-50 rounded-lg text-sm text-gray-700 transition-colors border border-gray-200 hover:border-purple-300"
            >
              "{example}"
            </button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
