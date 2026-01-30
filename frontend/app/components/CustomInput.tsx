"use client";

import React, { useState } from 'react';

interface CustomInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string;
}

export default function CustomInput({ label, value, ...props }: CustomInputProps) {
    return (
        <div className="input-container">
            <input
                className="input"
                placeholder=" "
                {...props}
            />
            <label className="input-label">
                {label}
            </label>
        </div>
    );
}
