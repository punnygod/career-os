"use client";

import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Option {
    value: string | number;
    label: string;
}

interface CustomSelectProps {
    label: string;
    options: Option[];
    value: string | number;
    onChange: (value: string | number) => void;
    placeholder?: string;
    required?: boolean;
}

export default function CustomSelect({ label, value, options, onChange, placeholder = "", required = false }: CustomSelectProps) {
    const [isOpen, setIsOpen] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    const selectedOption = options.find(opt => opt.value === value);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleSelect = (val: string | number) => {
        onChange(val);
        setIsOpen(false);
    };

    return (
        <div className="input-container relative" ref={containerRef}>
            <div
                onClick={() => setIsOpen(!isOpen)}
                className={`input min-h-[50px] flex items-center cursor-pointer ${isOpen ? 'border-indigo-500 shadow-[0_0_0_4px_#eef2ff] outline-none' : ''}`}
                data-has-value={!!value}
            >
                {selectedOption ? (
                    <span className="text-slate-900 font-medium z-10">{selectedOption.label}</span>
                ) : (
                    <span className="text-slate-400 z-10">{placeholder}</span>
                )}

                <div className="ml-auto pointer-events-none text-slate-400">
                    <ChevronDown size={18} className={`transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
                </div>
            </div>

            <label className={`input-label ${!!value || isOpen ? '-top-2.5 left-3 text-xs font-bold text-indigo-600 bg-white px-1 translate-y-0' : ''}`}>
                {label} {required && <span className="text-red-500">*</span>}
            </label>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        className="absolute z-50 w-full top-full left-0 mt-2 bg-white border border-slate-200 rounded-xl shadow-2xl max-h-60 overflow-y-auto"
                    >
                        {options.map(opt => (
                            <div
                                key={opt.value}
                                onClick={(e) => {
                                    e.stopPropagation();
                                    handleSelect(opt.value);
                                }}
                                className={`px-4 py-3 text-sm font-medium hover:bg-slate-50 cursor-pointer flex items-center justify-between group ${opt.value === value ? 'text-indigo-600 bg-indigo-50' : 'text-slate-700'
                                    }`}
                            >
                                {opt.label}
                                {opt.value === value && <Check size={16} className="text-indigo-600" />}
                            </div>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
