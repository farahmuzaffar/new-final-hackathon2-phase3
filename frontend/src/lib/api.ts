'use client';

import axios from 'axios';

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

// ================= AXIOS INSTANCE =================
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ================= REQUEST INTERCEPTOR =================
// Har request ke sath token attach karega
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers = config.headers ?? {};
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ================= RESPONSE INTERCEPTOR =================
// ❌ AUTO REDIRECT REMOVE (yehi tumhara bug tha)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      // ❌ window.location.href = '/login';  <-- YE HATA DIYA
    }
    return Promise.reject(error);
  }
);

// ================= TASK API =================
export const taskApi = {
  getTasks: async () => {
    const res = await apiClient.get('/api/tasks/');
    return res.data;
  },

  createTask: async (taskData: {
    title: string;
    description?: string;
  }) => {
    const res = await apiClient.post('/api/tasks/', taskData);
    return res.data;
  },

  updateTask: async (
    taskId: string,
    taskData: {
      title?: string;
      description?: string;
      completed?: boolean;
    }
  ) => {
    const res = await apiClient.put(`/api/tasks/${taskId}`, taskData);
    return res.data;
  },

  deleteTask: async (taskId: string) => {
    const res = await apiClient.delete(`/api/tasks/${taskId}`);
    return res.data;
  },
};

export default apiClient;
