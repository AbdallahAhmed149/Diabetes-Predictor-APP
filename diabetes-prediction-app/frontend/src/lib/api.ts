import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL!;

const api = axios.create({
    baseURL: `${API_URL}/api`,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    // Check if we're in the browser (not SSR)
    if (typeof window !== 'undefined') {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
    }
    return config;
});

// Auth API
export const authAPI = {
    register: (data: any) => api.post('/auth/register', data),
    login: (data: any) => api.post('/auth/login', data),
    getMe: () => api.get('/auth/me'),
    ensurePatient: () => api.post('/auth/me/ensure-patient'),
};

// Patients API
export const patientsAPI = {
    list: () => api.get('/patients/'),
    create: (data: any) => api.post('/patients/', data),
    get: (id: number) => api.get(`/patients/${id}/`),
    update: (id: number, data: any) => api.put(`/patients/${id}/`, data),
    delete: (id: number) => api.delete(`/patients/${id}/`),
};

// Predictions API
export const predictionsAPI = {
    create: (data: any) => api.post('/predictions/', data),
    list: () => api.get('/predictions/'),
    get: (id: number) => api.get(`/predictions/${id}/`),
    getByPatient: (patientId: number) => api.get(`/predictions/patient/${patientId}/`),
    downloadReport: (id: number) => api.get(`/predictions/${id}/report`, { responseType: 'blob' }),
};

export default api;
