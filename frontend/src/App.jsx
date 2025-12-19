import { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { FaChartLine, FaWallet, FaCreditCard, FaBullseye, FaShoppingBag } from 'react-icons/fa';
import Dashboard from './components/Dashboard';
import BudgetSection from './components/BudgetSection';
import ExpensesSection from './components/ExpensesSection';
import DebtsSection from './components/DebtsSection';
import GoalsSection from './components/GoalsSection';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const tabs = [
    { id: 'dashboard', label: 'Overview', icon: FaChartLine, desc: 'Your financial snapshot' },
    { id: 'budget', label: 'Budget', icon: FaWallet, desc: 'Plan your money' },
    { id: 'expenses', label: 'Expenses', icon: FaShoppingBag, desc: 'Track spending' },
    { id: 'debts', label: 'Debts', icon: FaCreditCard, desc: 'Payoff strategy' },
    { id: 'goals', label: 'Goals', icon: FaBullseye, desc: 'Save for dreams' },
  ];

  return (
    <div className="min-h-screen pb-10">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-500 rounded-xl flex items-center justify-center shadow-lg">
                <FaWallet className="text-white text-xl" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-500 bg-clip-text text-transparent">
                  FinanceFlow
                </h1>
                <p className="text-xs text-gray-500">Money made simple 💰</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Connected</span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm mt-4 mx-4 rounded-2xl overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="flex overflow-x-auto">
            {tabs.map(({ id, label, icon: Icon, desc }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`
                  flex flex-col items-center px-6 py-4 font-medium transition-all duration-300 flex-1 justify-center group
                  ${activeTab === id
                    ? 'text-primary-600 border-b-2 border-primary-600 bg-primary-50'
                    : 'text-gray-600 hover:text-primary-600 hover:bg-gray-50 hover:scale-105'
                  }
                `}
              >
                <Icon className={`text-2xl mb-1 transition-transform ${activeTab === id ? 'scale-110' : 'group-hover:scale-110'}`} />
                <span className="text-sm font-semibold">{label}</span>
                <span className="text-xs text-gray-400 mt-0.5 hidden sm:block">{desc}</span>
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div className="fade-in">
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'budget' && <BudgetSection />}
          {activeTab === 'expenses' && <ExpensesSection />}
          {activeTab === 'debts' && <DebtsSection />}
          {activeTab === 'goals' && <GoalsSection />}
        </div>
      </main>
    </div>
  );
}

export default App;
