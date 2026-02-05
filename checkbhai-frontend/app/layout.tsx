import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CheckBhai - AI Scam Detection for Bangladesh",
  description: "Protect yourself from scams with AI-powered detection. Check messages in English, Bangla, or Banglish.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-[#0a0a0c] text-white`}>
        <nav className="bg-[#0f0f13] border-b border-white/5 sticky top-0 z-50 backdrop-blur-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <a href="/" className="flex items-center gap-2">
                <span className="text-2xl">🛡️</span>
                <span className="text-xl font-black text-white tracking-tighter uppercase">CheckBhai</span>
              </a>
              <div className="flex gap-6 items-center">
                <a href="/report" className="text-red-500 hover:text-red-400 transition-colors font-black text-xs uppercase tracking-widest">
                  Report
                </a>
                <a href="/history" className="text-gray-400 hover:text-white transition-colors font-bold text-xs uppercase tracking-widest">
                  History
                </a>
                <a href="/payment" className="text-gray-400 hover:text-white transition-colors font-bold text-xs uppercase tracking-widest">
                  Payment
                </a>
                <a href="/admin" className="text-gray-400 hover:text-white transition-colors font-bold text-xs uppercase tracking-widest">
                  Admin
                </a>
              </div>
            </div>
          </div>
        </nav>
        <main className="min-h-screen">{children}</main>
        <footer className="bg-[#0f0f13] border-t border-white/5 text-gray-400 py-12 mt-20">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-[10px] font-bold uppercase tracking-widest">© 2026 CheckBhai &bull; Community-Powered Trust Infrastructure</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
