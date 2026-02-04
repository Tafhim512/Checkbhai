/**
 * CheckBhai API Client
 * Handles all backend API calls
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://checkbhai-production.up.railway.app';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests if available
apiClient.interceptors.request.use((config) => {
    if (typeof window !== 'undefined') {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
    }
    return config;
});

// API Methods
export const api = {
    // Auth
    register: async (email: string, password: string) => {
        const response = await apiClient.post('/auth/register', { email, password });
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
            localStorage.setItem('user_id', response.data.user_id);
            localStorage.setItem('is_admin', response.data.is_admin);
        }
        return response.data;
    },

    login: async (email: string, password: string) => {
        const response = await apiClient.post('/auth/login', { email, password });
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
            localStorage.setItem('user_id', response.data.user_id);
            localStorage.setItem('is_admin', response.data.is_admin);
        }
        return response.data;
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('is_admin');
    },

    isLoggedIn: () => {
        return typeof window !== 'undefined' && !!localStorage.getItem('token');
    },

    isAdmin: () => {
        return typeof window !== 'undefined' && localStorage.getItem('is_admin') === 'true';
    },

    // Check entity (Phone, bKash, Website, etc.)
    checkEntity: async (type: string, identifier: string) => {
        const response = await apiClient.get('/entities/check', {
            params: { type, identifier }
        });
        return response.data;
    },

    // Check message (Serverless via OpenAI)
    checkMessage: async (message: string) => {
        const response = await axios.post('/api/scamCheck', { message });
        return response.data;
    },

    // History
    getHistory: async (skip = 0, limit = 20, riskFilter?: string) => {
        const params: any = { skip, limit };
        if (riskFilter) params.risk_filter = riskFilter;
        const response = await apiClient.get('/history/', { params });
        return response.data;
    },

    getUserStats: async () => {
        const response = await apiClient.get('/history/stats');
        return response.data;
    },

    // Payment
    createPayment: async (paymentData: {
        amount: number;
        method: string;
        mobile_number?: string;
        account_number?: string;
        bank_name?: string;
    }) => {
        const response = await apiClient.post('/payment/', paymentData);
        return response.data;
    },

    getPaymentHistory: async () => {
        const response = await apiClient.get('/payment/history');
        return response.data;
    },

    // Admin
    getAdminStats: async () => {
        const response = await apiClient.get('/admin/stats');
        return response.data;
    },

    getAllMessages: async (skip = 0, limit = 50, riskFilter?: string) => {
        const params: any = { skip, limit };
        if (riskFilter) params.risk_filter = riskFilter;
        const response = await apiClient.get('/admin/messages', { params });
        return response.data;
    },

    retrainModel: async (trainingData: Array<{ text: string; label: string; category?: string }>) => {
        const response = await apiClient.post('/admin/retrain', { training_data: trainingData });
        return response.data;
    },

    getRecentActivity: async (limit = 10) => {
        const response = await apiClient.get('/admin/recent-activity', { params: { limit } });
        return response.data;
    },
};

export default api;
