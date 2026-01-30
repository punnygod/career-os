import axios from 'axios';
import type {
    Role,
    Question,
    Assessment,
    StartAssessmentResponse,
    CareerReport,
    Roadmap,
    AuthResponse,
    ProfileFormData,
    AnswerData,
    RoadmapWeek,
} from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests if available
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token} `;
    }
    return config;
});

// Roles API
export const rolesAPI = {
    getAll: async (): Promise<Role[]> => {
        const response = await api.get('/api/roles');
        return response.data;
    },
    getById: async (roleId: number): Promise<Role> => {
        const response = await api.get(`/api/roles/${roleId}`);
        return response.data;
    },
};

// Assessment API
export const assessmentAPI = {
    start: async (profileData: ProfileFormData): Promise<StartAssessmentResponse> => {
        const response = await api.post('/api/assessment/start', profileData);
        return response.data;
    },
    getQuestions: async (assessmentId: number): Promise<Question[]> => {
        const response = await api.get(`/api/assessment/${assessmentId}/questions`);
        return response.data;
    },
    submitAnswers: async (assessmentId: number, answers: Record<number, number>): Promise<void> => {
        await api.post(`/api/assessment/${assessmentId}/answers`, { answers });
    },
    complete: async (assessmentId: number): Promise<CareerReport> => {
        const response = await api.post(`/api/assessment/${assessmentId}/complete`);
        return response.data;
    },
};

// Report API
export const reportAPI = {
    get: async (assessmentId: number): Promise<CareerReport> => {
        const response = await api.get(`/api/report/${assessmentId}`);
        return response.data;
    },
    getRoadmap: async (assessmentId: number): Promise<Roadmap> => {
        const response = await api.get(`/api/report/${assessmentId}/roadmap`);
        const backendData = response.data;

        // Transform backend dict to frontend array
        const weeks: RoadmapWeek[] = [];
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        Object.entries(backendData.roadmap).forEach(([dimension, dimensionWeeks]: [string, any]) => {
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            dimensionWeeks.forEach((weekData: any) => {
                weeks.push({
                    week: weekData.week,
                    dimension: dimension,
                    tasks: weekData.tasks
                });
            });
        });

        // Sort by week
        weeks.sort((a, b) => a.week - b.week);

        return {
            assessment_id: backendData.assessment_id,
            weeks
        };
    },
};

// Auth API
export const authAPI = {
    register: async (email: string, password: string): Promise<AuthResponse> => {
        const response = await api.post('/api/auth/register', { email, password });
        return response.data;
    },
    login: async (email: string, password: string): Promise<AuthResponse> => {
        const response = await api.post('/api/auth/login', { email, password });
        return response.data;
    },
    saveAssessment: async (assessmentId: number): Promise<void> => {
        await api.post('/api/auth/save-assessment', { assessment_id: assessmentId });
    },
};

export default api;
