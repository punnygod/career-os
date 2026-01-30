'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  ArrowRight,
  BarChart3,
  Target,
  TrendingUp,
  ShieldCheck,
  Sparkles,
  Zap,
  CheckCircle2
} from 'lucide-react';
import GlassCard from './components/GlassCard';

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-slate-50">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
        <div className="container-custom h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
              <Sparkles size={18} className="text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight text-slate-900">Career OS</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">Features</a>
            <a href="#how-it-works" className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">How it Works</a>
          </div>
          <Link href="/assessment" className="btn btn-primary text-sm py-2 px-6">
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="relative pt-20 pb-24 overflow-hidden">
        <div className="container-custom relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <span className="badge badge-indigo mb-6 py-1 px-4">Beta Access Now Open</span>
              <h1 className="heading-xl mb-8">
                Master Your <span className="text-indigo-600">Growth Trajectory</span> as a Tech Professional
              </h1>
              <p className="text-xl text-slate-600 mb-10 max-w-2xl mx-auto leading-relaxed">
                Precision career intelligence tailored for engineers. Get benchmarked against the market, identify high-ROI skill gaps, and execute a verified path to seniority.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link href="/assessment" className="btn btn-primary text-lg px-10 py-4 w-full sm:w-auto group">
                  Start Free Assessment
                  <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
                </Link>
                <a href="#how-it-works" className="btn btn-secondary text-lg px-10 py-4 w-full sm:w-auto">
                  View Example Report
                </a>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-indigo-50 rounded-full blur-3xl -z-10 opacity-60" />
      </header>

      {/* Feature Grid */}
      <section id="features" className="py-24 bg-white">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="heading-l mb-4">Powerful Intelligence Tools</h2>
            <p className="text-slate-600 max-w-2xl mx-auto">Everything you need to navigate your career with confidence and clarity.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: <BarChart3 className="text-indigo-600" />,
                title: "Salary Benchmarking",
                desc: "Real-time market data matching your specific level, location, and tech stack."
              },
              {
                icon: <Target className="text-teal-600" />,
                title: "Skill Gap Analysis",
                desc: "Identify the critical dimension gaps holding you back from your next promotion."
              },
              {
                icon: <TrendingUp className="text-indigo-600" />,
                title: "ROI Roadmap",
                desc: "A personalized learning sequence optimized for the highest career leverage."
              }
            ].map((f, i) => (
              <GlassCard key={i} className="p-8 border-slate-100 hover:border-indigo-100 bg-slate-50/50">
                <div className="w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center mb-6">
                  {f.icon}
                </div>
                <h3 className="heading-m mb-3">{f.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{f.desc}</p>
              </GlassCard>
            ))}
          </div>
        </div>
      </section>

      {/* Social Proof / Trust */}
      <section className="py-20 border-t border-slate-100 bg-slate-50/30">
        <div className="container-custom">
          <div className="flex flex-col items-center gap-10">
            <p className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Built for Professionals from</p>
            <div className="flex flex-wrap justify-center gap-x-16 gap-y-8 grayscale opacity-50">
              <span className="text-2xl font-black text-slate-900 tracking-tighter">Google</span>
              <span className="text-2xl font-black text-slate-900 tracking-tighter">Meta</span>
              <span className="text-2xl font-black text-slate-900 tracking-tighter">Stripe</span>
              <span className="text-2xl font-black text-slate-900 tracking-tighter">Airbnb</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-slate-200 bg-white">
        <div className="container-custom">
          <div className="flex flex-col md:flex-row justify-between items-center gap-8">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-slate-900 rounded flex items-center justify-center">
                <Sparkles size={12} className="text-white" />
              </div>
              <span className="font-bold text-lg tracking-tight text-slate-900">Career OS</span>
            </div>
            <p className="text-sm text-slate-500">© 2026 Career OS. Professional Career Intelligence.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
