'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    LayoutDashboard,
    ClipboardCheck,
    Map,
    Settings,
    Target,
    ChevronRight
} from 'lucide-react';

const navItems = [
    { label: 'Dashboard', icon: LayoutDashboard, href: '/' },
    { label: 'Assessment', icon: ClipboardCheck, href: '/assessment' },
    { label: 'Roadmap', icon: Map, href: '/roadmap' },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="w-64 bg-slate-900 text-white h-screen sticky top-0 flex flex-col border-r border-slate-800">
            {/* Logo Section */}
            <div className="p-6 mb-2">
                <Link href="/" className="flex items-center gap-3 group">
                    <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-110 transition-transform">
                        <Target className="text-white" size={18} />
                    </div>
                    <span className="text-lg font-bold tracking-tight">
                        Career Intelligence
                    </span>
                </Link>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-3 space-y-1">
                {navItems.map((item) => {
                    const isActive = pathname === item.href;
                    const Icon = item.icon;

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`flex items-center justify-between px-3 py-2 rounded-md transition-all group ${isActive
                                    ? 'bg-slate-800 text-white'
                                    : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                                }`}
                        >
                            <div className="flex items-center gap-3">
                                <Icon size={18} className={isActive ? 'text-indigo-400' : 'group-hover:text-slate-200'} />
                                <span className="text-sm font-medium">{item.label}</span>
                            </div>
                            {isActive && <ChevronRight size={14} className="text-slate-500" />}
                        </Link>
                    );
                })}
            </nav>

            {/* Bottom Section */}
            <div className="p-4 border-t border-slate-800 mt-auto">
                <button className="flex items-center gap-3 px-3 py-2 w-full rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-all group">
                    <Settings size={18} className="group-hover:rotate-45 transition-transform" />
                    <span className="text-sm font-medium">Settings</span>
                </button>
                <div className="mt-4 px-3 py-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
                    <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1">Status</p>
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                        <span className="text-xs text-slate-300 font-medium">Market Data Live</span>
                    </div>
                </div>
            </div>
        </aside>
    );
}
