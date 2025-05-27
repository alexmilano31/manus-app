import axios from 'axios';

// Configuration de base
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://manus-app.onrender.com/api';

// Créer une instance axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token JWT à chaque requête
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs de réponse
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expiré ou invalide
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // Rediriger vers la page de connexion
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Services d'authentification
export const authService = {
  login: async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      const { access_token, user } = response.data;
      
      // Stocker le token et les infos utilisateur
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  register: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  },
  
  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },
  
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  }
};

// Services portfolio
export const portfolioService = {
  getBalance: async () => {
    try {
      const response = await api.get('/portfolio/balance');
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio balance:', error);
      throw error;
    }
  },
  
  getHistory: async () => {
    try {
      const response = await api.get('/portfolio/history');
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio history:', error);
      throw error;
    }
  },
  
  getPositions: async () => {
    try {
      const response = await api.get('/portfolio/positions');
      return response.data;
    } catch (error) {
      console.error('Error fetching portfolio positions:', error);
      throw error;
    }
  },
  
  addTransaction: async (transactionData) => {
    try {
      const response = await api.post('/portfolio/transactions', transactionData);
      return response.data;
    } catch (error) {
      console.error('Error adding transaction:', error);
      throw error;
    }
  }
};

// Services pour le market
export const marketService = {
  getMarketData: async () => {
    try {
      const response = await api.get('/market/data');
      return response.data;
    } catch (error) {
      console.error('Error fetching market data:', error);
      throw error;
    }
  },
  
  getCryptoPrices: async () => {
    try {
      const response = await api.get('/market/crypto-prices');
      return response.data;
    } catch (error) {
      console.error('Error fetching crypto prices:', error);
      throw error;
    }
  },
  
  getStockPrices: async () => {
    try {
      const response = await api.get('/market/stock-prices');
      return response.data;
    } catch (error) {
      console.error('Error fetching stock prices:', error);
      throw error;
    }
  }
};

export default api;