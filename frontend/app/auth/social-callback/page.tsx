"use client";

import { useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession } from "next-auth/react";
import { authAPI } from "@/app/lib/api";
import { Loader2 } from "lucide-react";

function SocialCallbackContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { data: session, status } = useSession();

  const redirect = searchParams.get("redirect") || "/assessment";
  const provider = searchParams.get("provider") || "social";

  useEffect(() => {
    const syncWithBackend = async () => {
      if (status !== "authenticated" || !session?.user?.email) return;

      try {
        const response = await authAPI.socialLogin(session.user.email, provider);
        if (typeof window !== "undefined") {
          localStorage.setItem("access_token", response.access_token);
          localStorage.setItem("user_email", response.email);
          localStorage.setItem("user_id", String(response.user_id));
        }
        router.replace(redirect);
      } catch (err) {
        console.error("Social login sync failed", err);
        router.replace(`/login?redirect=${encodeURIComponent(redirect)}`);
      }
    };

    void syncWithBackend();
  }, [status, session, provider, redirect, router]);

  return (
    <div className="flex flex-col items-center gap-3">
      <Loader2 className="w-6 h-6 text-indigo-600 animate-spin" />
      <p className="text-sm text-slate-600">
        Completing secure sign-in. Please wait...
      </p>
    </div>
  );
}

export default function SocialCallbackPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <Suspense fallback={
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="w-6 h-6 text-indigo-600 animate-spin" />
          <p className="text-sm text-slate-600">Loading...</p>
        </div>
      }>
        <SocialCallbackContent />
      </Suspense>
    </div>
  );
}

