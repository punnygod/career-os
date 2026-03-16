"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import Image from 'next/image';
import { motion } from 'framer-motion';
import {
  ArrowRight,
  BarChart3,
  Target,
  TrendingUp,
  ShieldCheck,
  Sparkles,
  Zap,
  CheckCircle2,
  Bot,
  Brain,
  Lightbulb,
} from 'lucide-react';
import GlassCard from './components/GlassCard';

export default function Home() {
  const router = useRouter();

  const handleStartAssessment = (redirectPath: string) => {
    const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
    if (!token) {
      router.push(`/login?redirect=${encodeURIComponent(redirectPath)}`);
    } else {
      router.push(redirectPath);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-slate-50">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
        <div className="container-custom h-16 flex items-center justify-between">
          <div className="flex items-center">
            <Image src="/logo.png" alt="Logo" width={80} height={80} />
            <span className="font-bold text-xl tracking-tight text-slate-900">Career OS</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">Features</a>
            <a href="#how-it-works" className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">How it Works</a>
          </div>
          <button
            type="button"
            className="btn btn-primary text-sm py-2 px-6"
            onClick={() => handleStartAssessment("/assessment")}
          >
            Get Started
          </button>
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
              <span className="badge badge-teal ml-2 py-1 px-4">
                AI-Powered Insights
              </span>
              <h1 className="heading-xl mb-8">
                Master Your <span className="text-indigo-600">Growth Trajectory</span> as a Tech Professional
              </h1>
              <p className="text-xl text-slate-600 mb-10 max-w-2xl mx-auto leading-relaxed">
                Precision career intelligence tailored for engineers. Get benchmarked against the market, identify high-ROI skill gaps, and execute a verified path to seniority.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <button
                  type="button"
                  className="btn btn-primary text-lg px-10 py-4 w-full sm:w-auto group"
                  onClick={() => handleStartAssessment("/assessment")}
                >
                  Start Free Assessment
                  <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
                </button>
                <Link href="/example-report" className="btn btn-secondary text-lg px-10 py-4 w-full sm:w-auto">
                  View Example Report
                </Link>
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

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
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
              },
              {
                icon: <Bot className="text-indigo-600" />,
                title: "AI Career Copilot",
                desc: "Personalized insights and recommendations generated from your profile."
              },
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
      {/* AI Highlight */}
      <section className="py-20 bg-slate-50">
        <div className="container-custom">
          <div className="text-center mb-12">
            <h2 className="heading-l mb-4">AI Career Copilot</h2>
            <p className="text-slate-600 max-w-2xl mx-auto">
              Combines intelligent models with market benchmarks to generate
              personalized career insights.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

            <GlassCard className="p-8 bg-white">
              <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center mb-6">
                <Brain className="text-indigo-600" size={24} />
              </div>
              <h3 className="heading-m mb-3">Smart Profile Analysis</h3>
              <p className="text-slate-600 text-sm">
                Understands your experience, stack, and goals.
              </p>
            </GlassCard>

            <GlassCard className="p-8 bg-white">
              <div className="w-12 h-12 rounded-xl bg-teal-50 flex items-center justify-center mb-6">
                <Lightbulb className="text-teal-600" size={24} />
              </div>
              <h3 className="heading-m mb-3">Actionable Suggestions</h3>
              <p className="text-slate-600 text-sm">
                Suggests skills, projects, and learning paths.
              </p>
            </GlassCard>

            <GlassCard className="p-8 bg-white">
              <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center mb-6">
                <Zap className="text-indigo-600" size={24} />
              </div>
              <h3 className="heading-m mb-3">Instant Reports</h3>
              <p className="text-slate-600 text-sm">
                Results generated within seconds.
              </p>
            </GlassCard>

          </div>
        </div>
      </section>


      {/* How It Works */}
      <section id="how-it-works" className="py-24 bg-slate-50">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="heading-l mb-4">The Career OS Protocol</h2>
            <p className="text-slate-600 max-w-2xl mx-auto">A data-driven approach to engineering career growth.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
            {/* Connecting lines for desktop */}
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-slate-200 -translate-y-1/2 -z-10" />

            {[
              { step: "01", title: "Select Track", desc: "Choose your professional domain for tailored benchmarking." },
              { step: "02", title: "Profile Data", desc: "Provide your experience, stack, and current market context." },
              { step: "03", title: "Assessment", desc: "Answer 50+ targeted questions across 10 depth dimensions." },
              { step: "04", title: "ROI Roadmap", desc: "Receive a verified path to your next salary and level jump." }
            ].map((s, i) => (
              <div key={i} className="flex flex-col items-center text-center group">
                <div className="w-16 h-16 rounded-full bg-white border-4 border-slate-50 flex items-center justify-center text-xl font-black text-indigo-600 shadow-sm mb-6 group-hover:scale-110 transition-transform">
                  {s.step}
                </div>
                <h3 className="text-lg font-bold mb-2">{s.title}</h3>
                <p className="text-sm text-slate-500">{s.desc}</p>
              </div>
            ))}
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
              <span className="font-bold text-lg tracking-tight text-slate-900">AI-Powered Career Intelligence.
              </span>
            </div>
            <p className="text-sm text-slate-500">© 2026 Career OS. Professional Career Intelligence.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
