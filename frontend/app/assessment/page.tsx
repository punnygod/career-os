"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from 'framer-motion';
import {
    rolesAPI,
    assessmentAPI,
    profileAPI
} from '@/app/lib/api';
import type { Role, Question, ProfileFormData, Stack, Certificate } from '@/app/types';
import GlassCard from '../components/GlassCard';
import CustomInput from '../components/CustomInput';
import CustomSelect from '../components/CustomSelect';
import MultiSelect from '../components/MultiSelect';
import {
    Sparkles,
    ArrowRight,
    ChevronLeft,
    Loader2,
    CheckCircle2,
    AlertCircle,
    Target,
    BarChart3,
    Monitor,
    Server,
    Layers,
    Cloud
} from 'lucide-react';
import Image from 'next/image';

type Step = 'role' | 'profile' | 'questions' | 'loading' | 'error';

export default function Assessment() {
    const router = useRouter();
    const [step, setStep] = useState<Step>('role');
    const [roles, setRoles] = useState<Role[]>([]);
    const [stacks, setStacks] = useState<Stack[]>([]);
    const [certificates, setCertificates] = useState<Certificate[]>([]);
    const [questions, setQuestions] = useState<Question[]>([]);
    const [selectedRole, setSelectedRole] = useState<number | null>(null);
    const [profileData, setProfileData] = useState<Partial<ProfileFormData>>({});
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState<Record<number, number>>({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [assessmentId, setAssessmentId] = useState<number | null>(null);

    useEffect(() => {
        const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
        if (!token) {
            router.replace(`/login?redirect=${encodeURIComponent("/assessment")}`);
            return;
        }

        loadRoles();
        loadStacks();
        loadCertificates();
    }, [router]);

    const loadCertificates = async () => {
        try {
            const data = await profileAPI.getCertificates();
            setCertificates(data);
        } catch (err) {
            console.error('Failed to load certificates:', err);
        }
    };

    const loadStacks = async () => {
        try {
            const data = await profileAPI.getStacks();
            setStacks(data);
        } catch (err) {
            console.error('Failed to load stacks:', err);
        }
    };

    const loadRoles = async () => {
        try {
            const data = await rolesAPI.getAll();
            setRoles(data);
        } catch (err) {
            console.error(err);
            setError('Failed to load roles. Please refresh the page.');
            setStep('error');
        }
    };

    const handleRoleSelect = (roleId: number) => {
        setSelectedRole(roleId);
    };

    const handleProfileSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setStep('loading');
        try {
            const fullProfile: ProfileFormData = {
                role_id: selectedRole!,
                years_of_experience: profileData.years_of_experience || 0,
                company_type: profileData.company_type || 'Product',
                current_salary: profileData.current_salary || 0,
                target_role: profileData.target_role || '',
                location: profileData.location,
                current_level: profileData.current_level,
                tech_stack: profileData.tech_stack || [],
                certifications: profileData.certifications || []
            };
            const startRes = await assessmentAPI.start(fullProfile);
            setAssessmentId(startRes.assessment_id);
            const data = await assessmentAPI.getQuestions(startRes.assessment_id);
            setQuestions(data);
            setStep('questions');
        } catch (err) {
            console.error(err);
            setError('Failed to initialize assessment. Please try again.');
            setStep('error');
        }
    };

    const handleAnswer = (score: number) => {
        const questionId = questions[currentQuestionIndex].id;
        setAnswers(prev => ({ ...prev, [questionId]: score }));

        if (currentQuestionIndex < questions.length - 1) {
            setTimeout(() => {
                setCurrentQuestionIndex(prev => prev + 1);
            }, 300);
        }
    };

    const handleSubmitAssessment = async () => {
        if (!assessmentId) return;
        setIsSubmitting(true);
        setStep('loading');
        try {
            await assessmentAPI.submitAnswers(assessmentId, answers);
            await assessmentAPI.complete(assessmentId);
            router.push(`/dashboard/${assessmentId}`);
        } catch (err) {
            console.error(err);
            setError('Submission failed. Please try again.');
            setStep('error');
            setIsSubmitting(false);
        }
    };

    const progress = questions.length > 0
        ? ((Object.keys(answers).length) / questions.length) * 100
        : 0;

    const getRoleIcon = (roleName: string) => {
        const name = roleName.toLowerCase();
        if (name.includes('frontend')) return <Monitor size={24} />;
        if (name.includes('backend')) return <Server size={24} />;
        if (name.includes('full')) return <Layers size={24} />;
        if (name.includes('devops')) return <Cloud size={24} />;
        return <Target size={24} />;
    };

    return (
        <div className="min-h-screen bg-slate-50 py-12 px-6">
            <div className="max-w-4xl mx-auto">
                {/* Global Progress Indicator */}
                <div className="flex justify-between items-center mb-12">
                    <div className="flex items-center">
                        <Image src="/logo.png" alt="Career OS" width={100} height={100} />
                        <div>
                            <h2 className="text-sm font-bold text-slate-900">Career OS</h2>
                            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Protocol v1.0</p>
                        </div>
                    </div>
                </div>

                <AnimatePresence mode="wait">
                    {step === 'role' && (
                        <motion.div
                            key="role"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="space-y-8"
                        >
                            <div className="text-center max-w-2xl mx-auto">
                                <h1 className="heading-l mb-4">Choose Your Track</h1>
                                <p className="text-slate-500 font-medium">
                                    Our intelligence engine adapts to your specific professional domain for accurate benchmarking.
                                </p>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {roles.map((role) => (
                                    <GlassCard
                                        key={role.id}
                                        onClick={() => handleRoleSelect(role.id)}
                                        className={`p-8 border-2 text-center transition-all ${selectedRole === role.id
                                            ? 'border-indigo-600 bg-white shadow-xl shadow-indigo-100'
                                            : 'border-white hover:border-slate-200 bg-white/60'
                                            }`}
                                    >
                                        <div className={`mx-auto w-12 h-12 rounded-2xl flex items-center justify-center mb-6 transition-colors ${selectedRole === role.id ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-400'
                                            }`}>
                                            {getRoleIcon(role.name)}
                                        </div>
                                        <h3 className={`text-xl font-bold mb-2 ${selectedRole === role.id ? 'text-slate-900' : 'text-slate-700'}`}>{role.name}</h3>
                                        <p className="text-sm text-slate-500 leading-relaxed font-medium">{role.description}</p>
                                    </GlassCard>
                                ))}
                            </div>

                            <div className="flex justify-center pt-6">
                                <button
                                    onClick={() => selectedRole && setStep('profile')}
                                    disabled={!selectedRole}
                                    className="btn btn-primary px-12 py-4 text-base group"
                                >
                                    Continue to Profile
                                    <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
                                </button>
                            </div>
                        </motion.div>
                    )}

                    {step === 'profile' && (
                        <motion.div
                            key="profile"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            className="space-y-8"
                        >
                            <button
                                onClick={() => setStep('role')}
                                className="flex items-center text-xs font-bold text-slate-400 hover:text-indigo-600 transition-colors uppercase tracking-widest"
                            >
                                <ChevronLeft size={14} className="mr-1" /> Back
                            </button>

                            <div className="text-center max-w-2xl mx-auto">
                                <h1 className="heading-l mb-4">Market Context</h1>
                                <p className="text-slate-500 font-medium">
                                    Provide baseline data to help us calculate your current percentile and growth potential.
                                </p>
                            </div>

                            <GlassCard className="p-8 md:p-12 bg-white">
                                <form onSubmit={handleProfileSubmit} className="space-y-8">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-2">
                                        <CustomInput
                                            label="Years of Experience"
                                            type="number" step="0.5" min="0" max="50" required
                                            value={profileData.years_of_experience || ''}
                                            onChange={(e) => setProfileData(p => ({ ...p, years_of_experience: parseFloat(e.target.value) }))}
                                        />

                                        <CustomSelect
                                            label="Company Type"
                                            required
                                            value={profileData.company_type || ''}
                                            onChange={(val) => setProfileData(p => ({ ...p, company_type: val as any }))}
                                            options={[
                                                { value: "Product", label: "Product" },
                                                { value: "Service", label: "Service" },
                                                { value: "Startup", label: "Startup" },
                                                { value: "MNC", label: "MNC" }
                                            ]}
                                        />

                                        <CustomInput
                                            label="Current Annual Salary (INR)"
                                            type="number" min="0" required
                                            value={profileData.current_salary || ''}
                                            onChange={(e) => setProfileData(p => ({ ...p, current_salary: parseInt(e.target.value) }))}
                                        />

                                        <CustomInput
                                            label="Target Level / Title"
                                            type="text" required
                                            value={profileData.target_role || ''}
                                            onChange={(e) => setProfileData(p => ({ ...p, target_role: e.target.value }))}
                                        />

                                        <CustomInput
                                            label="Current Level (Optional)"
                                            type="text"
                                            placeholder="Senior SWE, L5, etc."
                                            value={profileData.current_level || ''}
                                            onChange={(e) => setProfileData(p => ({ ...p, current_level: e.target.value }))}
                                        />

                                        <CustomInput
                                            label="Location (Optional)"
                                            type="text"
                                            placeholder="San Francisco, Remote, etc."
                                            value={profileData.location || ''}
                                            onChange={(e) => setProfileData(p => ({ ...p, location: e.target.value }))}
                                        />

                                        <MultiSelect
                                            label=""
                                            options={stacks.map(s => ({ id: s.name, label: s.name }))}
                                            selectedValues={profileData.tech_stack || []}
                                            placeholder="Select your core technologies..."
                                            required
                                            onChange={(values) => setProfileData(p => ({
                                                ...p,
                                                tech_stack: values as string[]
                                            }))}
                                        />

                                        <MultiSelect
                                            label="Certifications"
                                            options={certificates.map(c => ({ id: c.name, label: c.name }))}
                                            selectedValues={profileData.certifications || []}
                                            placeholder="AWS, Azure, GCP, etc."
                                            onChange={(values) => setProfileData(p => ({
                                                ...p,
                                                certifications: values as string[]
                                            }))}
                                        />
                                    </div>

                                    <div className="pt-4">
                                        <button type="submit" className="btn btn-primary w-full py-4 text-base">
                                            Generate Assessment Focus
                                            <Sparkles className="ml-2" size={18} />
                                        </button>
                                    </div>
                                </form>
                            </GlassCard>
                        </motion.div>
                    )}

                    {step === 'questions' && (
                        <motion.div
                            key="questions"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="space-y-10"
                        >
                            {/* Question Progress Header */}
                            <div className="fixed top-0 left-0 w-full h-1 bg-slate-200 z-[60]">
                                <motion.div
                                    className="h-full bg-indigo-600"
                                    initial={{ width: 0 }}
                                    animate={{ width: `${progress}%` }}
                                />
                            </div>

                            <div className="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border border-slate-100">
                                <div className="flex items-center gap-3">
                                    <span className="px-3 py-1 bg-indigo-50 text-indigo-700 rounded-lg text-xs font-black uppercase tracking-widest">
                                        Question {currentQuestionIndex + 1}/{questions.length}
                                    </span>
                                    <span className="text-xs font-bold text-slate-400 border-l border-slate-200 pl-3">
                                        {questions[currentQuestionIndex].dimension}
                                    </span>
                                </div>
                                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                                    Focus: Skill Mapping
                                </span>
                            </div>

                            <div className="bg-white p-8 md:p-12 rounded-3xl shadow-xl shadow-slate-200/60 border border-slate-100 min-h-[400px] flex flex-col justify-center">
                                <h1 className="text-2xl md:text-3xl font-bold text-slate-900 mb-12 text-center leading-tight">
                                    {questions[currentQuestionIndex].question_text}
                                </h1>

                                <div className="grid grid-cols-1 gap-4 max-w-lg mx-auto w-full">
                                    {[1, 2, 3, 4, 5].map((score) => (
                                        <button
                                            key={score}
                                            onClick={() => handleAnswer(score)}
                                            className={`group relative flex items-center justify-between p-5 rounded-2xl border-2 transition-all duration-300 text-left ${answers[questions[currentQuestionIndex].id] === score
                                                ? 'border-indigo-600 bg-indigo-50/50 shadow-lg shadow-indigo-100'
                                                : 'border-slate-100 hover:border-slate-200 hover:bg-slate-50'
                                                }`}
                                        >
                                            <span className={`font-bold transition-colors ${answers[questions[currentQuestionIndex].id] === score ? 'text-indigo-700' : 'text-slate-600'
                                                }`}>
                                                {score === 1 && 'Novice / Beginner'}
                                                {score === 2 && 'Learning / Practical'}
                                                {score === 3 && 'Competent / Independent'}
                                                {score === 4 && 'Proficient / Mentor'}
                                                {score === 5 && 'Expert / Thought Leader'}
                                            </span>
                                            <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all ${answers[questions[currentQuestionIndex].id] === score
                                                ? 'bg-indigo-600 border-indigo-600'
                                                : 'border-slate-200 bg-white'
                                                }`}>
                                                {answers[questions[currentQuestionIndex].id] === score && <CheckCircle2 size={14} className="text-white" />}
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div className="flex justify-between items-center pt-4">
                                <button
                                    onClick={() => setCurrentQuestionIndex(p => Math.max(0, p - 1))}
                                    disabled={currentQuestionIndex === 0}
                                    className="flex items-center gap-2 text-sm font-bold text-slate-400 hover:text-slate-600 transition-colors disabled:opacity-0"
                                >
                                    <ChevronLeft size={16} /> Previous
                                </button>

                                {Object.keys(answers).length === questions.length ? (
                                    <button
                                        onClick={handleSubmitAssessment}
                                        disabled={isSubmitting}
                                        className="btn btn-primary px-12 py-4 shadow-xl shadow-indigo-200 flex items-center gap-2"
                                    >
                                        {isSubmitting ? <Loader2 className="animate-spin" /> : <BarChart3 size={18} />}
                                        Finalize Analysis
                                    </button>
                                ) : (
                                    <div className="text-xs font-bold text-slate-400 uppercase tracking-widest">
                                        Auto-advancing on selection
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    )}

                    {step === 'loading' && (
                        <motion.div
                            key="loading"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex flex-col items-center justify-center py-24 space-y-8"
                        >
                            <div className="relative">
                                <Loader2 className="w-16 h-16 text-indigo-600 animate-spin" />
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <Sparkles size={24} className="text-indigo-400 animate-pulse" />
                                </div>
                            </div>
                            <div className="text-center">
                                <h2 className="text-2xl font-bold text-slate-900 mb-2">Analyzing Trajectory...</h2>
                                <p className="text-slate-500 font-medium">Crunching market data and dimension scoring.</p>
                            </div>
                        </motion.div>
                    )}

                    {step === 'error' && (
                        <motion.div
                            key="error"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="text-center py-20 px-8 bg-white rounded-3xl border-2 border-red-50"
                        >
                            <div className="w-16 h-16 bg-red-50 text-red-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                                <AlertCircle size={32} />
                            </div>
                            <h2 className="text-2xl font-bold text-slate-900 mb-2">Protocol Interrupted</h2>
                            <p className="text-slate-500 mb-8 max-w-sm mx-auto">{error}</p>
                            <button
                                onClick={() => window.location.reload()}
                                className="btn btn-primary"
                            >
                                Restart Assessment
                            </button>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
