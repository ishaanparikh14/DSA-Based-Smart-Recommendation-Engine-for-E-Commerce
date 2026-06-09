/**
 * API Client for Backend Communication
 * Base URL: http://localhost:5000
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Products
export const getProducts = (category = null, q = null) => {
  const params = {};
  if (category && category !== 'All') params.category = category;
  if (q) params.q = q;
  return api.get('/products', { params });
};

export const getProduct = (id) => api.get(`/products/${id}`);

// Users
export const getUsers = () => api.get('/users');

export const getUser = (userId) => api.get(`/users/${userId}`);

// Recommendations
export const getRecommendations = (userId, k = 10, explain = false) => {
  return api.get(`/recommendations/${userId}`, {
    params: { k, explain },
  });
};

export const explainRecommendation = (userId, productId) => {
  return api.get(`/recommendations/${userId}/explain/${productId}`);
};

export const getFrequentlyBoughtTogether = (productId, k = 5) => {
  return api.get(`/frequently-bought-together/${productId}`, {
    params: { k },
  });
};

// Cart
export const addToCart = (userId, productId, quantity = 1) => {
  return api.post(`/cart/${userId}/add`, { product_id: productId, quantity });
};

export const removeFromCart = (userId, productId) => {
  return api.post(`/cart/${userId}/remove`, { product_id: productId });
};

export const updateCartQuantity = (userId, productId, quantity) => {
  return api.post(`/cart/${userId}/update-quantity`, { product_id: productId, quantity });
};

export const getCart = (userId) => api.get(`/cart/${userId}`);

// Views
export const trackView = (userId, productId) => {
  return api.post(`/view/${userId}/${productId}`);
};

export const getRecentViews = (userId) => api.get(`/recent-views/${userId}`);

export const popView = (userId) => {
  return api.post(`/view/${userId}/pop`);
};

export const getSessionQueue = (userId) => api.get(`/session-queue/${userId}`);

export const dequeueSessionItem = (userId) => {
  return api.post(`/session-queue/${userId}/dequeue`);
};

// Pricing
export const getDynamicPrice = (productId, userId = null) => {
  const params = userId ? { user_id: userId } : {};
  return api.get(`/pricing/${productId}`, { params });
};

// Categories
export const getCategories = () => api.get('/categories');

// DSA Activity
export const getDSAActivity = (limit = 20) => {
  return api.get('/dsa-activity', { params: { limit } });
};

export const logDSAActivity = (operation, dataStructure, details) => {
  return api.post('/dsa-activity/log', {
    operation,
    data_structure: dataStructure,
    details
  });
};

// Recommendation Graph Visualization
export const getRecommendationGraph = (userId) => {
  return api.get(`/visualize/recommendation-graph/${userId}`);
};

// User-Product Graph Visualization
export const getUserProductGraph = (userId) => {
  return api.get(`/visualize/user-product-graph/${userId}`);
};

// User Similarity Complete Graph
export const getUserSimilarityGraph = () => {
  return api.get('/visualize/user-similarity-graph');
};

// User Order History Graph
export const getUserOrderHistory = (userId) => {
  return api.get(`/visualize/user-orders/${userId}`);
};

// Stats
export const getStats = () => api.get('/stats');

// Health Check
export const healthCheck = () => api.get('/health');

export default api;
