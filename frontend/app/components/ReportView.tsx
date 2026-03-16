'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import {
    Zap,
    CheckCircle2,
    ChevronRight,
    TrendingUp,
    BarChart3,
    Target,
    Sparkles,
    ArrowRight
} from 'lucide-react';
import type { CareerReport } from '@/app/types';
import ScoreGauge from './ScoreGauge';
import DimensionRadar from './DimensionRadar';
import GlassCard from './GlassCard';

interface ReportViewProps {
    report: CareerReport;
    assessmentId?: string | number;
    isExample?: boolean;
}

export default function ReportView({ report, assessmentId, isExample = false }: ReportViewProps) {
    return (
        <div className="min-h-screen bg-slate-50 py-12 px-6">
            <div className="max-w-7xl mx-auto space-y-10">
                {/* Header */}
                <header className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                    <div>
                        <div className="flex items-center gap-2 mb-2">
                            <span className="badge badge-indigo">Analysis Complete</span>
                            {assessmentId && <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">Assessment ID: #{assessmentId}</span>}
                            {isExample && <span className="text-xs font-bold text-teal-500 uppercase tracking-widest">Example Report</span>}
                        </div>
                        <h1 className="heading-l">Career <span className="text-indigo-600">Intelligence</span> Report</h1>
                        <p className="text-slate-500 font-medium">Your personalized trajectory analysis and market positioning.</p>
                    </div>
                    <div className="flex gap-4">
                        {!isExample ? (
                            <Link href={`/roadmap/${assessmentId}`} className="btn btn-primary px-8 py-3">
                                Execute Roadmap
                                <ArrowRight className="ml-2" size={18} />
                            </Link>
                        ) : (
                            <Link href="/assessment" className="btn btn-primary px-8 py-3">
                                Start Your Assessment
                                <ArrowRight className="ml-2" size={18} />
                            </Link>
                        )}
                    </div>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* Primary Score & Summary */}
                    <div className="lg:col-span-4 space-y-8">
                        <GlassCard className="p-10 text-center flex flex-col items-center bg-white">
                            <ScoreGauge score={report.overall_score} size="lg" label="Overall Readiness" />
                            <div className="mt-8 space-y-4 w-full">
                                <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100 flex items-center justify-between">
                                    <span className="text-sm font-bold text-slate-500">Readiness Level</span>
                                    <span className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-lg text-xs font-black uppercase tracking-widest">
                                        {report.readiness_level}
                                    </span>
                                </div>
                                <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100 flex items-center justify-between">
                                    <span className="text-sm font-bold text-slate-500">Market Profile</span>
                                    <span className="text-sm font-bold text-slate-900">{report.company_fit}</span>
                                </div>
                            </div>
                        </GlassCard>

                        <GlassCard className="p-8 bg-indigo-600 text-white">
                            <div className="flex items-center gap-3 mb-6">
                                <Zap className="text-indigo-300" size={24} />
                                <h3 className="text-xl font-bold">Quick Wins</h3>
                            </div>
                            <ul className="space-y-4">
                                {report.quick_wins.map((win, i) => (
                                    <li key={i} className="flex gap-3 text-sm font-medium leading-relaxed">
                                        <CheckCircle2 size={18} className="text-indigo-300 flex-shrink-0 mt-0.5" />
                                        {win}
                                    </li>
                                ))}
                            </ul>
                            {!isExample && (
                                <Link href={`/roadmap/${assessmentId}`} className="mt-8 flex items-center justify-center gap-2 p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-colors text-sm font-bold border border-white/10">
                                    View Full Execution Plan <ChevronRight size={16} />
                                </Link>
                            )}
                        </GlassCard>
                    </div>

                    {/* Detailed Analysis & Charts */}
                    <div className="lg:col-span-8 space-y-8">
                        {/* Financial Impact Bar */}
                        {report.salary_info && (
                            <GlassCard className="p-8 bg-white border-2 border-indigo-50">
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 divide-y md:divide-y-0 md:divide-x divide-slate-100">
                                    <div className="flex flex-col gap-1 items-center md:items-start">
                                        <span className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Market Potential</span>
                                        <div className="flex items-baseline gap-1 text-slate-900">
                                            <span className="text-3xl font-black">₹{report.salary_info.expected_median.toLocaleString('en-IN')}</span>
                                            <span className="text-xs font-bold text-slate-400">/YR</span>
                                        </div>
                                    </div>
                                    <div className="flex flex-col gap-1 items-center md:items-start md:pl-8 pt-6 md:pt-0">
                                        <span className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Salary Delta</span>
                                        <div className="flex items-center gap-2 text-indigo-600">
                                            <TrendingUp size={24} />
                                            <span className="text-3xl font-black">{(report.salary_info.gap || 0) < 0 ? '-' : '+'}₹{Math.abs(report.salary_info.gap || 0).toLocaleString('en-IN')}</span>
                                        </div>
                                    </div>
                                    <div className="flex flex-col gap-1 items-center md:items-start md:pl-8 pt-6 md:pt-0">
                                        <span className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Alignment Status</span>
                                        <span className={`text-xl font-bold ${['Aligned', 'Optimized', 'Market Leader'].includes(report.salary_info.alignment)
                                            ? 'text-teal-600'
                                            : 'text-amber-600'
                                            }`}>
                                            {report.salary_info.alignment}
                                        </span>
                                    </div>
                                </div>
                            </GlassCard>
                        )}

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            <GlassCard className="p-8 bg-white overflow-hidden flex flex-col items-center">
                                <div className="w-full flex justify-between items-center mb-6">
                                    <div>
                                        <h3 className="text-lg font-bold text-slate-900">Dimension Chart</h3>
                                        <p className="text-xs text-slate-500 font-medium">Core skill distribution</p>
                                    </div>
                                    <div className="w-8 h-8 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600">
                                        <BarChart3 size={18} />
                                    </div>
                                </div>
                                <div className="w-full py-6">
                                    <DimensionRadar data={report.radar_chart_data} />
                                </div>
                            </GlassCard>

                            <GlassCard className="p-8 bg-white max-h-[600px] overflow-y-auto custom-scrollbar">
                                <div className="w-full flex justify-between items-center mb-8 sticky top-0 bg-white z-10 py-2">
                                    <div>
                                        <h3 className="text-lg font-bold text-slate-900">Dimension Breakdown</h3>
                                        <p className="text-xs text-slate-500 font-medium">Detailed scoring audit</p>
                                    </div>
                                    <div className="w-8 h-8 rounded-lg bg-teal-50 flex items-center justify-center text-teal-600">
                                        <Target size={18} />
                                    </div>
                                </div>
                                <div className="space-y-8">
                                    {/* Group scores by category */}
                                    {Object.entries(
                                        report.dimension_scores.reduce((acc, ds) => {
                                            if (!acc[ds.category]) acc[ds.category] = [];
                                            acc[ds.category].push(ds);
                                            return acc;
                                        }, {} as Record<string, typeof report.dimension_scores>)
                                    ).map(([category, scores]) => (
                                        <div key={category} className="space-y-4">
                                            <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] border-b border-slate-100 pb-2">
                                                {category}
                                            </h4>
                                            <div className="space-y-5">
                                                {scores.map((ds, i) => (
                                                    <div key={ds.dimension} className="group">
                                                        <div className="flex justify-between items-end mb-2">
                                                            <span className="text-sm font-bold text-slate-700">{ds.dimension}</span>
                                                            <span className={`text-xs font-black ${ds.score >= 80 ? 'text-teal-600' : ds.score >= 60 ? 'text-indigo-600' : 'text-amber-600'}`}>{Math.round(ds.score)}%</span>
                                                        </div>
                                                        <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                                                            <motion.div
                                                                initial={{ width: 0 }}
                                                                animate={{ width: `${ds.score}%` }}
                                                                transition={{ duration: 1 }}
                                                                className={`h-full ${ds.score >= 80 ? 'bg-teal-500' : ds.score >= 60 ? 'bg-indigo-500' : 'bg-amber-500'}`}
                                                            />
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </GlassCard>
                        </div>

                        {/* Analysis Detail */}
                        <GlassCard className="p-8 bg-slate-900 text-white overflow-hidden relative">
                            <div className="relative z-10">
                                <div className="flex items-center gap-3 mb-4">
                                    <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-indigo-400">
                                        <Sparkles size={20} />
                                    </div>
                                    <h3 className="text-xl font-bold">AI Path Analysis</h3>
                                </div>
                                <p className="text-slate-400 text-sm leading-relaxed max-w-2xl mb-6">
                                    {report.company_fit_explanation}
                                </p>
                                <div className="flex flex-wrap gap-3">
                                    {report.weak_dimensions.map((dim, i) => (
                                        <span key={i} className="px-3 py-1 bg-white/5 border border-white/10 rounded-lg text-[10px] font-black uppercase tracking-widest text-indigo-300">
                                            Priority: {dim}
                                        </span>
                                    ))}
                                </div>
                            </div>
                            {/* Bg Decor */}
                            <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 blur-[80px] rounded-full" />
                        </GlassCard>
                    </div>
                </div>
            </div>
        </div>
    );
}
