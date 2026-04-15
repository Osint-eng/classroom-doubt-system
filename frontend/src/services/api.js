import axios from 'axios';

const API_URL = 'https://classroom-doubt-system-8.onrender.com/api';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const register = (userData) => api.post('/auth/register', userData);
export const login = (credentials) => api.post('/auth/login', credentials);
export const getCurrentUser = () => api.get('/auth/me');
export const getQuestions = () => api.get('/questions');
export const getQuestionById = (id) => api.get(`/questions/${id}`);  // Make sure this has /questions/
export const createQuestion = (data) => api.post('/questions', data);
export const addAnswer = (questionId, content) => api.post(`/answers/${questionId}`, { content });
export const voteAnswer = (answerId, voteType) => api.post(`/answers/${answerId}/vote`, { vote_type: voteType });
export const acceptAnswer = (answerId) => api.put(`/answers/${answerId}/accept`);
export const getDashboard = () => api.get('/users/dashboard');

export default api;
