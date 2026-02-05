/**
 * CheckBhai API Client
 * Handles all backend API calls for Community-Powered Trust Platform
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://checkbhai.onrender.com';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000, // 30 second timeout for Render cold starts
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
    // Health check
    healthCheck: async (): Promise<{ status: string; service: string } | null> => {
        try {
            const response = await apiClient.get('/health', { timeout: 10000 });
            return response.data;
        } catch (error) {
            console.error('Health check failed:', error);
            return null;
        }
    },

    isBackendReachable: async (): Promise<boolean> => {
        const health = await api.healthCheck();
        return health !== null && health.status === 'ok';
    },

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

    // Check entity - returns community trust data
    checkEntity: async (type: string, identifier: string) => {
        const response = await apiClient.get('/entities/check', {
            params: { type, identifier }
        });
        return response.data;
    },

    // Check message - for suspicious message analysis
    checkMessage: async (message: string) => {
        try {
            const response = await apiClient.post('/check/message', { message });
            return response.data;
        } catch (error: any) {
            console.error('Message check failed:', error.message);
            throw new Error('Backend unreachable. Please try again later.');
        }
    },

    // Submit a scam report
    submitReport: async (reportData: {
        entity_id: string;
        platform: string;
        scam_type: string;
        amount_lost: number;
        description: string;
        evidence: Array<{ file_url: string; file_type: string }>;
    }) => {
        const response = await apiClient.post('/reports/', reportData);
        return response.data;
    },

    // Get reports for an entity
    getEntityReports: async (entityId: string) => {
        const response = await apiClient.get(`/entities/${entityId}/reports`);
        return response.data;
    },

    // Get entity details by ID
    getEntityDetails: async (entityId: string) => {
        const response = await apiClient.get(`/entities/${entityId}`);
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

    // Payment (placeholder for future)
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

    getAdminReports: async (skip = 0, limit = 50, statusFilter?: string) => {
        const params: any = { skip, limit };
        if (statusFilter) params.status_filter = statusFilter;
        const response = await apiClient.get('/admin/reports', { params });
        return response.data;
    },

    verifyReport: async (reportId: string) => {
        const response = await apiClient.put(`/admin/reports/${reportId}/verify`);
        return response.data;
    },

    deleteReport: async (reportId: string) => {
        const response = await apiClient.delete(`/admin/reports/${reportId}`);
        return response.data;
    },

    // Track premium CTA clicks (for validation)
    trackPremiumClick: async () => {
        try {
            // For now, just log - can be enhanced later
            console.log('Premium CTA clicked');
        } catch (error) {
            // Silent fail
        }
    }
};

export default api;
