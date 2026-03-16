'use client';

import { motion } from 'framer-motion';

interface ScoreGaugeProps {
    score: number; // 0-100
    label?: string;
    size?: 'sm' | 'md' | 'lg';
}

export default function ScoreGauge({ score, label, size = 'md' }: ScoreGaugeProps) {
    const sizeClasses = {
        sm: { container: 'w-24 h-24', text: 'text-2xl', stroke: 6, radius: 40 },
        md: { container: 'w-32 h-32', text: 'text-4xl', stroke: 8, radius: 45 },
        lg: { container: 'w-48 h-48', text: 'text-6xl', stroke: 10, radius: 45 },
    };

    const config = sizeClasses[size];
    const circumference = 2 * Math.PI * config.radius;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    return (
        <div className="flex flex-col items-center gap-2">
            <div className={`relative ${config.container}`}>
                <svg className="transform -rotate-90 w-full h-full drop-shadow-[0_0_15px_rgba(79,70,229,0.3)]" viewBox="0 0 100 100">
                    {/* Track */}
                    <circle
                        cx="50"
                        cy="50"
                        r={config.radius}
                        stroke="#f1f5f9" // slate-100
                        strokeWidth={config.stroke}
                        fill="none"
                    />
                    {/* Progress with gradient-like shadow */}
                    <motion.circle
                        cx="50"
                        cy="50"
                        r={config.radius}
                        stroke="#4f46e5" // indigo-600
                        strokeWidth={config.stroke}
                        fill="none"
                        strokeLinecap="round"
                        strokeDasharray={circumference}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset }}
                        transition={{ duration: 1.5, ease: 'easeOut' }}
                    />
                </svg>

                {/* Score Text */}
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`${config.text} font-black text-slate-900`}>
                        {Math.round(score)}
                    </span>
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Score</span>
                </div>
            </div>

            {label && (
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">{label}</span>
            )}
        </div>
    );
}
