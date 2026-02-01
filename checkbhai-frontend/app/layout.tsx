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
      <body className={inter.className}>
        <nav className="bg-white shadow-md sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <a href="/" className="flex items-center gap-2">
                <span className="text-2xl">🛡️</span>
                <span className="text-xl font-bold gradient-text">CheckBhai</span>
              </a>
              <div className="flex gap-4">
                <a href="/history" className="text-gray-700 hover:text-primary-600 transition-colors">
                  History
                </a>
                <a href="/payment" className="text-gray-700 hover:text-primary-600 transition-colors">
                  Payment
                </a>
                <a href="/admin" className="text-gray-700 hover:text-primary-600 transition-colors">
                  Admin
                </a>
              </div>
            </div>
          </div>
        </nav>
        <main className="min-h-screen">{children}</main>
        <footer className="bg-gray-800 text-white py-8 mt-16">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-sm">© 2026 CheckBhai. Protecting Bangladesh from scams with AI.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
