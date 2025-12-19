import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Budget
export const createBudget = (data) => api.post('/budget', data);
export const getBudget = () => api.get('/budget');

// Expenses
export const createExpense = (data) => api.post('/expenses', data);
export const getExpenses = () => api.get('/expenses');
export const getExpenseSummary = () => api.get('/expenses/summary');
export const resetExpenses = (beforeDate = null) => {
  const params = beforeDate ? { before_date: beforeDate } : {};
  return api.delete('/expenses/reset', { params });
};

// Debts
export const createDebt = (data) => api.post('/debts', data);
export const getDebts = () => api.get('/debts');
export const getPayoffPlan = (method = 'avalanche') => api.get(`/debts/payoff-plan?method=${method}`);

// Goals
export const createGoal = (data) => api.post('/goals', data);
export const getGoals = () => api.get('/goals');

// Dashboard
export const getDashboardStats = () => api.get('/dashboard/stats');

export default api;
