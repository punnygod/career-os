'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Target } from 'lucide-react';

export default function Navbar() {
    const pathname = usePathname();

    const isActive = (path: string) => pathname === path;

    return (
        <nav className="glass-strong border-b border-white/5 sticky top-0 z-50 py-2">
            <div className="container-custom">
                <div className="flex items-center justify-between h-20">
                    {/* Logo */}
                    <Link href="/" className="flex items-center gap-3 group">
                        <div className="w-12 h-12 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg shadow-primary/20 group-hover:shadow-primary/40 transition-all">
                            <Target className="text-white" size={28} />
                        </div>
                        <span className="text-2xl font-bold text-white group-hover:text-gradient transition-all tracking-tight">
                            Career OS
                        </span>
                    </Link>

                    {/* Navigation Links */}
                    <div className="hidden md:flex items-center gap-6">
                        <Link
                            href="/"
                            className={`text-sm font-medium transition-colors ${isActive('/')
                                ? 'text-white'
                                : 'text-gray-400 hover:text-white'
                                }`}
                        >
                            Home
                        </Link>
                        <Link
                            href="/assessment"
                            className={`text-sm font-medium transition-colors ${isActive('/assessment')
                                ? 'text-white'
                                : 'text-gray-400 hover:text-white'
                                }`}
                        >
                            Assessment
                        </Link>
                    </div>

                    {/* CTA Button */}
                    <div className="flex items-center gap-4">
                        <Link href="/assessment" className="btn btn-primary text-sm px-6 py-2">
                            Start Assessment
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
}
