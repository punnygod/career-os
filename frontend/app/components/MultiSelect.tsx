'use client';

import React, { useState, useRef, useEffect } from 'react';
import { X, ChevronDown, Check } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Option {
    id: string | number;
    label: string;
}

interface MultiSelectProps {
    label: string;
    options: Option[];
    selectedValues: (string | number)[];
    onChange: (values: (string | number)[]) => void;
    placeholder?: string;
    required?: boolean;
}

export default function MultiSelect({
    label,
    options,
    selectedValues,
    onChange,
    placeholder = "Select options...",
    required = false
}: MultiSelectProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const containerRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    const selectedOptions = options.filter(opt => selectedValues.includes(opt.id));
    const filteredOptions = options.filter(opt =>
        opt.label.toLowerCase().includes(searchTerm.toLowerCase()) &&
        !selectedValues.includes(opt.id)
    );

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleRemove = (id: string | number, e: React.MouseEvent) => {
        e.stopPropagation();
        onChange(selectedValues.filter(v => v !== id));
    };

    const handleSelect = (id: string | number) => {
        onChange([...selectedValues, id]);
        setSearchTerm('');
        inputRef.current?.focus();
    };

    const hasValue = selectedValues.length > 0 || isOpen || searchTerm.length > 0;

    return (
        <div className="input-container relative" ref={containerRef}>
            <div
                onClick={() => {
                    setIsOpen(true);
                    inputRef.current?.focus();
                }}
                className={`input min-h-[50px] h-auto flex flex-wrap gap-2 items-center cursor-text ${isOpen ? 'border-indigo-500 shadow-[0_0_0_4px_#eef2ff] outline-none' : ''}`}
                data-has-value={hasValue}
            >
                {selectedOptions.length === 0 && !isOpen && !label && (
                    <span className="text-slate-400 text-sm ml-1 select-none">{placeholder}</span>
                )}

                <AnimatePresence>
                    {selectedOptions.map(opt => (
                        <motion.span
                            key={opt.id}
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.8, opacity: 0 }}
                            className="inline-flex items-center bg-indigo-600 text-white text-xs font-bold px-2 py-1 rounded-lg shadow-sm group whitespace-nowrap z-10"
                        >
                            {opt.label}
                            <button
                                onClick={(e) => handleRemove(opt.id, e)}
                                className="ml-1 hover:bg-indigo-500 rounded-full p-0.5 transition-colors"
                            >
                                <X size={10} />
                            </button>
                        </motion.span>
                    ))}
                </AnimatePresence>

                {isOpen && (
                    <input
                        ref={inputRef}
                        autoFocus
                        type="text"
                        className="flex-1 bg-transparent border-none outline-none text-sm min-w-[120px] p-1 text-slate-700 placeholder:text-slate-400"
                        placeholder={placeholder || "Search..."}
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        onClick={(e) => e.stopPropagation()}
                    />
                )}
                <div className="ml-auto pointer-events-none text-slate-400">
                    <ChevronDown size={18} className={`transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
                </div>
            </div>

            <label className={`input-label ${hasValue ? '-top-2.5 left-3 text-xs font-bold text-indigo-600 bg-white px-1 translate-y-0' : ''}`}>
                {label}
            </label>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        className="absolute z-50 w-full top-full left-0 mt-2 bg-white border border-slate-200 rounded-xl shadow-2xl max-h-60 overflow-y-auto"
                    >
                        {filteredOptions.length > 0 ? (
                            filteredOptions.map(opt => (
                                <div
                                    key={opt.id}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        handleSelect(opt.id);
                                    }}
                                    className="px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50 cursor-pointer flex items-center justify-between group"
                                >
                                    {opt.label}
                                    <Check size={16} className="text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity" />
                                </div>
                            ))
                        ) : (
                            <div className="px-4 py-8 text-center">
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">No matching options</p>
                            </div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
