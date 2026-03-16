"use client";

import { signIn } from "next-auth/react";
import { Github, Mail, Chrome } from "lucide-react";

interface AuthProvidersProps {
  redirectPath?: string;
}

export default function AuthProviders({ redirectPath = "/assessment" }: AuthProvidersProps) {
  const callbackUrl = `/auth/social-callback?redirect=${encodeURIComponent(redirectPath)}`;

  return (
    <div className="space-y-2">
      <button
        type="button"
        onClick={() => signIn("google", { callbackUrl })}
        className="w-full flex items-center justify-center gap-2 rounded-lg border border-slate-200 bg-white text-slate-800 text-sm font-semibold py-2.5 hover:bg-slate-50 transition-colors"
      >
        <Chrome className="w-4 h-4" />
        Continue with Google
      </button>
      <button
        type="button"
        onClick={() => signIn("github", { callbackUrl })}
        className="w-full flex items-center justify-center gap-2 rounded-lg border border-slate-200 bg-slate-900 text-white text-sm font-semibold py-2.5 hover:bg-slate-800 transition-colors"
      >
        <Github className="w-4 h-4" />
        Continue with GitHub
      </button>
      <div className="flex items-center gap-2 my-2">
        <div className="flex-1 h-px bg-slate-200" />
        <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-widest">
          Or continue with email
        </span>
        <div className="flex-1 h-px bg-slate-200" />
      </div>
    </div>
  );
}

