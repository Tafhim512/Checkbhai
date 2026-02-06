import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CheckBhai - Community-Powered Trust Platform for Bangladesh",
  description: "Bangladesh's Anti-Scam & Fraud Verification Layer. Check before you pay. Community-powered trust intelligence.",
  keywords: ["scam detection", "bangladesh", "fraud", "bkash", "nagad", "trust", "verification"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-[#0a0a0c] text-white`}>
        <nav className="bg-[#0f0f13]/90 border-b border-white/5 sticky top-0 z-50 backdrop-blur-xl">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <a href="/" className="flex items-center gap-2 group">
                <span className="text-2xl group-hover:scale-110 transition-transform">🛡️</span>
                <span className="text-xl font-black text-white tracking-tighter uppercase">CheckBhai</span>
              </a>
              <div className="flex gap-4 md:gap-6 items-center overflow-x-auto">
                <a href="/report" className="text-red-500 hover:text-red-400 transition-colors font-black text-[10px] md:text-xs uppercase tracking-widest whitespace-nowrap">
                  Report
                </a>
                <a href="/network" className="text-gray-400 hover:text-white transition-colors font-bold text-[10px] md:text-xs uppercase tracking-widest whitespace-nowrap hidden md:block">
                  Network
                </a>
                <a href="/history" className="text-gray-400 hover:text-white transition-colors font-bold text-[10px] md:text-xs uppercase tracking-widest whitespace-nowrap">
                  History
                </a>
                <a href="/payment" className="text-gray-400 hover:text-white transition-colors font-bold text-[10px] md:text-xs uppercase tracking-widest whitespace-nowrap hidden md:block">
                  Premium
                </a>
                <a href="/admin" className="text-gray-400 hover:text-white transition-colors font-bold text-[10px] md:text-xs uppercase tracking-widest whitespace-nowrap">
                  Admin
                </a>
              </div>
            </div>
          </div>
        </nav>
        <main className="min-h-screen">{children}</main>
        <footer className="bg-[#0f0f13] border-t border-white/5 text-gray-400 py-12 mt-20">
          <div className="max-w-7xl mx-auto px-4 text-center space-y-4">
            <p className="text-[10px] font-bold uppercase tracking-widest">© 2026 CheckBhai &bull; Community-Powered Trust Infrastructure</p>
            <p className="text-[9px] text-gray-600 max-w-xl mx-auto">
              Disclaimer: CheckBhai provides community-sourced risk information. This is not a legal verdict. 
              Always verify through official channels before making financial decisions.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
