// Core Types
export interface Role {
    id: number;
    name: string;
    description: string;
}

export interface Stack {
    id: number;
    name: string;
    description: string;
    multiplier: number;
}

export interface Certificate {
    id: number;
    name: string;
    provider: string;
    multiplier: number;
}

export interface Question {
    id: number;
    role_id: number;
    dimension: string;
    question_text: string;
    answer_options: number[];
}

export interface Assessment {
    id: number;
    user_id?: number;
    role_id: number;
    years_of_experience: number;
    company_type: string;
    current_salary: number;
    target_role: string;
    answers: Record<string, number>;
    scores: Record<string, number>;
    overall_score: number;
    completed: boolean;
    created_at: string;
}

export interface DimensionScore {
    dimension: string;
    category: string;
    score: number;
    status: string;
}

export interface SalaryInfo {
    current?: number;
    expected_min: number;
    expected_max: number;
    expected_median: number;
    alignment: string;
    gap?: number;
}

export interface RadarChartItem {
    dimension: string;
    user_score: number;
    benchmark_score: number;
}

export interface LearningResource {
    title: string;
    type: string;
    url: string;
}

export interface NextLevelPreview {
    target_role: string;
    target_level: string;
    salary_min: number;
    salary_max: number;
}

export interface CareerReport {
    assessment_id: number;
    overall_score: number;
    readiness_level: string;
    dimension_scores: DimensionScore[];
    salary_info: SalaryInfo | null;
    company_fit: string;
    company_fit_explanation: string;
    weak_dimensions: string[];
    quick_wins: string[];
    radar_chart_data: RadarChartItem[];
    interview_questions: string[];
    learning_resources: LearningResource[];
    next_level_preview?: NextLevelPreview;
    location?: string;
    tech_stack?: string[];
    current_level?: string;
}

export interface RoadmapWeek {
    week: number;
    dimension: string;
    tasks: string[];
}

export interface Roadmap {
    assessment_id: number;
    weeks: RoadmapWeek[];
}

export interface User {
    id: number;
    email: string;
    created_at: string;
}

export interface StartAssessmentResponse {
    assessment_id: number;
    session_id: string;
    message: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
    user_id: number;
    email: string;
}

// Form Types
export interface ProfileFormData {
    role_id: number;
    years_of_experience: number;
    company_type: 'Service' | 'Startup' | 'Product' | 'MNC';
    current_salary: number;
    target_role: string;
    location?: string;
    tech_stack?: string[];
    certifications?: string[];
    current_level?: string;
}

export interface AnswerData {
    question_id: number;
    answer: number;
}
