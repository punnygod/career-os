'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import {
    reportAPI
} from '@/app/lib/api';
import type { CareerReport } from '@/app/types';
import {
    Loader2,
    AlertCircle,
} from 'lucide-react';
import Link from 'next/link';
import ReportView from '@/app/components/ReportView';

export default function Dashboard() {
    const { assessmentId } = useParams();
    const router = useRouter();
    const [report, setReport] = useState<CareerReport | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (assessmentId) {
            loadReport();
        }
    }, [assessmentId]);

    const loadReport = async () => {
        try {
            const data = await reportAPI.get(parseInt(assessmentId as string));
            setReport(data);
        } catch (err) {
            console.error(err);
            setError('Failed to load report. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 gap-6">
                <Loader2 className="w-12 h-12 text-indigo-600 animate-spin" />
                <p className="text-slate-500 font-medium">Generating your career intelligence report...</p>
            </div>
        );
    }

    if (error || !report) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-slate-50">
                <div className="text-center p-12 bg-white rounded-3xl shadow-xl border border-slate-100 max-w-md">
                    <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-6" />
                    <h2 className="text-2xl font-bold text-slate-900 mb-2">Report Unavailable</h2>
                    <p className="text-slate-500 mb-8">{error || 'Could not find the requested assessment.'}</p>
                    <Link href="/assessment" className="btn btn-primary w-full">
                        Start New Assessment
                    </Link>
                </div>
            </div>
        );
    }

    return <ReportView report={report} assessmentId={assessmentId as string} />;
}
