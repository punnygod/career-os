'use client';

import ReportView from '@/app/components/ReportView';
import type { CareerReport } from '@/app/types';

const EXAMPLE_REPORT: CareerReport = {
    assessment_id: 0,
    overall_score: 85,
    readiness_level: "High",
    dimension_scores: [
        { dimension: "System Design", category: "Technical", score: 88, status: "Advanced" },
        { dimension: "Architecture", category: "Technical", score: 82, status: "Advanced" },
        { dimension: "Coding Standards", category: "Technical", score: 90, status: "Expert" },
        { dimension: "Leadership", category: "Soft Skills", score: 75, status: "Intermediate" },
        { dimension: "Communication", category: "Soft Skills", score: 85, status: "Advanced" },
        { dimension: "Product Sense", category: "Product", score: 78, status: "Intermediate" },
        { dimension: "Strategic Thinking", category: "Product", score: 70, status: "Intermediate" }
    ],
    salary_info: {
        expected_min: 4500000,
        expected_max: 6500000,
        expected_median: 5500000,
        alignment: "Optimized",
        gap: 1200000,
        current: 4300000
    },
    company_fit: "Product-Led Growth Startup",
    company_fit_explanation: "Your profile strongly matches with Series B+ Product startups that value high engineering velocity combined with strong product sense. You show exceptional capability in pure engineering execution but have room to grow in strategic leadership roles.",
    weak_dimensions: ["Strategic Thinking", "Leadership"],
    quick_wins: [
        "Lead a cross-functional architectural review within the next 30 days.",
        "Mentor 2 junior engineers on advanced system patterns.",
        "Contribute to product roadmap discussions to improve product sense."
    ],
    radar_chart_data: [
        { dimension: "System Design", user_score: 88, benchmark_score: 75 },
        { dimension: "Architecture", user_score: 82, benchmark_score: 70 },
        { dimension: "Coding", user_score: 90, benchmark_score: 80 },
        { dimension: "Leadership", user_score: 75, benchmark_score: 65 },
        { dimension: "Communication", user_score: 85, benchmark_score: 75 },
        { dimension: "Product", user_score: 78, benchmark_score: 70 }
    ],
    interview_questions: [],
    learning_resources: []
};

export default function ExampleReportPage() {
    return <ReportView report={EXAMPLE_REPORT} isExample={true} />;
}
