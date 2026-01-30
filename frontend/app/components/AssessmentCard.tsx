'use client';

import { motion } from 'framer-motion';

interface AssessmentCardProps {
    question: string;
    questionNumber: number;
    totalQuestions: number;
    dimension: string;
    selectedAnswer: number | null;
    onAnswerSelect: (answer: number) => void;
}

const answerOptions = [
    { value: 1, label: 'Not at all', color: 'bg-slate-50 border-slate-200' },
    { value: 2, label: 'Occasionally', color: 'bg-slate-50 border-slate-200' },
    { value: 3, label: 'Frequently', color: 'bg-slate-50 border-slate-200' },
    { value: 4, label: 'Consistently', color: 'bg-slate-50 border-slate-200' },
];

export default function AssessmentCard({
    question,
    questionNumber,
    totalQuestions,
    dimension,
    selectedAnswer,
    onAnswerSelect,
}: AssessmentCardProps) {
    return (
        <div className="w-full max-w-2xl mx-auto space-y-8">
            {/* Header / Info */}
            <div className="flex items-center justify-between">
                <div className="flex flex-col">
                    <span className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1">Dimension</span>
                    <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded uppercase">{dimension}</span>
                </div>
                <div className="text-right flex flex-col items-end">
                    <span className="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1">Progress</span>
                    <span className="text-xs font-bold text-slate-900">{Math.round((questionNumber / totalQuestions) * 100)}%</span>
                </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <motion.div
                    className="h-full bg-indigo-600"
                    initial={{ width: 0 }}
                    animate={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
                />
            </div>

            {/* Question Area */}
            <div className="card p-8 bg-white border-slate-200 shadow-sm">
                <h3 className="heading-3 mb-10 text-slate-900 leading-tight">
                    {question}
                </h3>

                {/* Options */}
                <div className="grid grid-cols-1 gap-3">
                    {answerOptions.map((option) => (
                        <button
                            key={option.value}
                            onClick={() => onAnswerSelect(option.value)}
                            className={`flex items-center justify-between p-4 rounded-xl border focus:outline-none transition-all ${selectedAnswer === option.value
                                    ? 'bg-indigo-50 border-indigo-600 ring-2 ring-indigo-600/10'
                                    : 'bg-white border-slate-200 hover:border-slate-300'
                                }`}
                        >
                            <div className="flex items-center gap-4">
                                <div className={`w-10 h-10 rounded-lg flex items-center justify-center font-bold text-sm transition-colors ${selectedAnswer === option.value ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600'
                                    }`}>
                                    {option.value}
                                </div>
                                <span className={`text-sm font-bold transition-colors ${selectedAnswer === option.value ? 'text-indigo-900' : 'text-slate-700'
                                    }`}>
                                    {option.label}
                                </span>
                            </div>

                            <div className={`w-5 h-5 rounded-full border flex items-center justify-center transition-all ${selectedAnswer === option.value ? 'bg-indigo-600 border-indigo-600' : 'border-slate-300'
                                }`}>
                                {selectedAnswer === option.value && (
                                    <div className="w-1.5 h-1.5 rounded-full bg-white" />
                                )}
                            </div>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}
