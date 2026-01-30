'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import {
    reportAPI
} from '@/app/lib/api';
import type { Roadmap } from '@/app/types';
import GlassCard from '@/app/components/GlassCard';
import {
    Loader2,
    ChevronLeft,
    Calendar,
    CheckCircle2,
    Circle,
    ArrowRight,
    Target,
    Zap,
    Rocket,
    Brain,
    ShieldCheck,
    Sparkles
} from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function RoadmapPage() {
    const { assessmentId } = useParams();
    const [roadmap, setRoadmap] = useState<Roadmap | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (assessmentId) {
            loadRoadmap();
        }
    }, [assessmentId]);

    const loadRoadmap = async () => {
        try {
            const data = await reportAPI.getRoadmap(parseInt(assessmentId as string));
            setRoadmap(data);
        } catch (err) {
            console.error(err);
            setError('Failed to load your roadmap. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 gap-6">
                <Loader2 className="w-12 h-12 text-indigo-600 animate-spin" />
                <p className="text-slate-500 font-medium">Building your execution roadmap...</p>
            </div>
        );
    }

    if (error || !roadmap) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-slate-50">
                <div className="text-center p-12 bg-white rounded-3xl shadow-xl border border-slate-100 max-w-md">
                    <h2 className="text-2xl font-bold text-slate-900 mb-2">Roadmap Missing</h2>
                    <p className="text-slate-500 mb-8">{error || 'Could not find the requested roadmap.'}</p>
                    <Link href={`/dashboard/${assessmentId}`} className="btn btn-primary w-full">
                        Return to Dashboard
                    </Link>
                </div>
            </div>
        );
    }

    // Group tasks by week
    const weeks = Array.from(new Set(roadmap.weeks.map(w => w.week))).sort((a, b) => a - b);

    return (
        <div className="min-h-screen bg-slate-50 py-12 px-6">
            <div className="max-w-4xl mx-auto space-y-10">
                <header className="space-y-6">
                    <Link href={`/dashboard/${assessmentId}`} className="flex items-center text-xs font-bold text-slate-400 hover:text-indigo-600 transition-colors uppercase tracking-widest">
                        <ChevronLeft size={14} className="mr-1" /> Back to Intelligence Report
                    </Link>

                    <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
                        <div>
                            <div className="flex items-center gap-2 mb-2">
                                <Calendar className="text-indigo-600" size={18} />
                                <span className="text-xs font-black text-slate-400 uppercase tracking-widest">4-Week Execution Protocol</span>
                            </div>
                            <h1 className="heading-l">Growth <span className="text-indigo-600">Roadmap</span></h1>
                            <p className="text-slate-500 font-medium">Your step-by-step sequence to bridge critical dimension gaps.</p>
                        </div>
                        <div className="flex -space-x-2">
                            {[Rocket, Brain, Target, ShieldCheck].map((Icon, i) => (
                                <div key={i} className="w-10 h-10 rounded-full border-2 border-white bg-slate-100 flex items-center justify-center text-slate-400 shadow-sm">
                                    <Icon size={18} />
                                </div>
                            ))}
                        </div>
                    </div>
                </header>

                <div className="relative">
                    {/* Vertical Line */}
                    <div className="absolute left-[19px] top-6 bottom-6 w-[2px] bg-slate-200 hidden md:block" />

                    <div className="space-y-12">
                        {weeks.map((weekNum, idx) => {
                            const weekTasks = roadmap.weeks.filter(w => w.week === weekNum);
                            return (
                                <motion.div
                                    key={weekNum}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: idx * 0.1 }}
                                    className="relative flex flex-col md:flex-row gap-8"
                                >
                                    {/* Week Indicator */}
                                    <div className="relative z-10 flex-shrink-0">
                                        <div className="w-10 h-10 rounded-full bg-white border-2 border-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-100 outline outline-4 outline-slate-50">
                                            <span className="text-xs font-black text-indigo-600">{weekNum}</span>
                                        </div>
                                    </div>

                                    {/* Content Card */}
                                    <div className="flex-grow space-y-4">
                                        <div className="flex items-center gap-3">
                                            <h2 className="text-lg font-black text-slate-900 uppercase tracking-tight">Week {weekNum}</h2>
                                            <div className="h-[1px] flex-grow bg-slate-100" />
                                            <span className="text-[10px] font-black text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded uppercase tracking-widest italic">Phase: Acceleration</span>
                                        </div>

                                        <div className="grid grid-cols-1 gap-4">
                                            {weekTasks.map((dimensionGroup, dIdx) => (
                                                <GlassCard key={dIdx} className="p-8 bg-white border-slate-100 hover:border-indigo-100 transition-all group">
                                                    <div className="flex items-center gap-3 mb-6">
                                                        <div className="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-indigo-50 group-hover:text-indigo-600 transition-colors">
                                                            <Target size={16} />
                                                        </div>
                                                        <span className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">{dimensionGroup.dimension}</span>
                                                    </div>

                                                    <div className="space-y-4">
                                                        {dimensionGroup.tasks.map((task, tIdx) => (
                                                            <div key={tIdx} className="flex gap-4 group/item">
                                                                <button className="flex-shrink-0 mt-0.5 w-5 h-5 rounded border border-slate-200 flex items-center justify-center bg-white hover:border-indigo-400 hover:bg-indigo-50 transition-all text-transparent hover:text-indigo-600">
                                                                    <CheckCircle2 size={12} />
                                                                </button>
                                                                <p className="text-sm font-medium text-slate-600 leading-relaxed group-hover/item:text-slate-900 transition-colors">{task}</p>
                                                            </div>
                                                        ))}
                                                    </div>
                                                </GlassCard>
                                            ))}
                                        </div>
                                    </div>
                                </motion.div>
                            );
                        })}
                    </div>
                </div>

                <div className="pt-10 flex justify-center">
                    <GlassCard className="p-8 bg-slate-900 text-white max-w-2xl w-full text-center relative overflow-hidden group">
                        <div className="relative z-10">
                            <Sparkles className="mx-auto mb-4 text-indigo-400 group-hover:scale-110 transition-transform" size={32} />
                            <h3 className="text-xl font-bold mb-2">Build Your Expert Portfolio</h3>
                            <p className="text-slate-400 text-sm mb-8 leading-relaxed">
                                Document your progress through this roadmap to create a "Proof of Work" artifact that significantly increases your leverage during next compensation review.
                            </p>
                            <button className="btn btn-primary px-8 py-3">
                                Download Protocol PDF
                            </button>
                        </div>
                        <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 blur-[60px] rounded-full" />
                    </GlassCard>
                </div>
            </div>
        </div>
    );
}
