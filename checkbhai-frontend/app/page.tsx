/**
 * CheckBhai Home Page - Community-Powered Trust Intelligence Platform
 */

'use client';

import EntitySearch from '@/components/EntitySearch';

export default function Home() {
  return (
    <div className="relative min-h-screen bg-[#0a0a0c] text-white overflow-hidden">
      {/* Background Glows */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/20 blur-[120px] rounded-full pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-red-600/10 blur-[120px] rounded-full pointer-events-none"></div>

      {/* Main Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-6 pt-24 pb-32 flex flex-col items-center">

        {/* Badge */}
        <div className="mb-8 px-4 py-1.5 bg-blue-500/10 border border-blue-500/20 rounded-full flex items-center gap-2 animate-fade-in">
          <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(59,130,246,0.8)]"></span>
          <span className="text-[10px] font-bold uppercase tracking-widest text-blue-400">Community-Powered Trust Platform</span>
        </div>

        {/* Hero Title */}
        <div className="text-center mb-16 space-y-4 max-w-4xl">
          <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-none mb-6">
            <span className="text-white">CHECK</span>
            <span className="text-blue-600 block md:inline md:ml-4 italic">BHAI / ভাই</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-400 font-medium leading-relaxed">
            The place people check before sending money. Community-powered trust intelligence for Bangladesh.
          </p>
        </div>

        {/* Unified Search Engine */}
        <div className="w-full mb-24 animate-slide-up">
          <div className="text-center mb-8">
            <h2 className="text-sm font-bold uppercase tracking-[0.3em] text-gray-500">Search Before You Pay</h2>
          </div>
          <EntitySearch />
        </div>

        {/* Features / Value Props */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full mt-12 pb-12 border-b border-white/5">
          <ValueCard
            icon="👥"
            title="Community Reports"
            desc="Real reports from real users. No fake certainty - just honest data from the community."
          />
          <ValueCard
            icon="📊"
            title="Trust Signals"
            desc="See risk level, report count, and verification status. Make informed decisions."
          />
          <ValueCard
            icon="🔒"
            title="Append-Only"
            desc="Every report is permanent. Scammers cannot erase their history."
          />
        </div>

        {/* Bottom CTA / Stats */}
        <div className="mt-24 text-center max-w-2xl">
          <p className="text-gray-400 text-sm font-medium mb-12">
            HELPING BANGLADESH MAKE SAFER TRANSACTIONS
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button
              onClick={() => window.location.href = '/report'}
              className="bg-red-600 text-white font-black py-4 px-10 rounded-2xl hover:bg-red-700 transition-all"
            >
              🚩 Report a Scam
            </button>
            <button className="bg-transparent text-white border border-white/20 font-black py-4 px-10 rounded-2xl hover:bg-white/5 transition-all">
              Premium Coming Soon
            </button>
          </div>
        </div>
      </div>

      {/* Footer Branding */}
      <footer className="relative z-10 py-12 text-center text-gray-600 font-bold text-xs uppercase tracking-widest">
        &copy; 2026 CHECKBHAI &bull; COMMUNITY-POWERED TRUST PLATFORM
      </footer>
    </div>
  );
}

function ValueCard({ icon, title, desc }: { icon: string; title: string; desc: string }) {
  return (
    <div className="p-8 rounded-3xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.04] transition-all group">
      <div className="text-4xl mb-6 group-hover:scale-110 transition-transform origin-left">{icon}</div>
      <h3 className="text-xl font-bold mb-3 text-white">{title}</h3>
      <p className="text-gray-500 text-sm leading-relaxed">{desc}</p>
    </div>
  );
}
