import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Sidebar from "./components/Sidebar";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Career OS - Career Intelligence for Tech Professionals",
  description: "Get personalized career assessments, salary benchmarking, and actionable growth roadmaps to accelerate your tech career.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} font-sans antialiased bg-slate-50 text-slate-900`}
      >
        <div className="min-h-screen">
          <main className="w-full">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
