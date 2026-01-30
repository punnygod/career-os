"use client";

import React from 'react';

interface GlassCardProps {
    children: React.ReactNode;
    className?: string;
    onClick?: () => void;
}

const GlassCard = ({ children, className = '', onClick }: GlassCardProps) => {
    return (
        <div
            onClick={onClick}
            className={`card ${onClick ? 'cursor-pointer card-hover active:scale-[0.99]' : ''} ${className}`}
        >
            {children}
        </div>
    );
};

export default GlassCard;
