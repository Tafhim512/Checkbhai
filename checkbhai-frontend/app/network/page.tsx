"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function NetworkPage() {
    const [loading, setLoading] = useState(false);
    const [networkData, setNetworkData] = useState<any[]>([]);

    // For MVP, we'll fetch mock or basic detection results
    useEffect(() => {
        // In a real flow, we'd pass an entity ID to explore
    }, []);

    return (
        <div className="min-h-screen bg-[#0a0a0c] text-white p-6 md:p-12">
            <div className="max-w-6xl mx-auto">
                <div className="flex justify-between items-end mb-12">
                    <div>
                        <h1 className="text-5xl font-black tracking-tighter">NETWORK DETECTION</h1>
                        <p className="text-gray-500 font-bold uppercase text-xs tracking-[0.4em] mt-2">Cross-Entity Fraud Analysis</p>
                    </div>
                    <div className="hidden md:block text-right">
                        <span className="text-[10px] font-black text-blue-500 uppercase tracking-widest border border-blue-500/30 px-3 py-1 rounded-full">AI Experimental</span>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Main Visualization Area */}
                    <div className="lg:col-span-2 bg-white/[0.02] border border-white/5 rounded-3xl p-8 min-h-[500px] flex flex-col items-center justify-center relative overflow-hidden">
                        <div className="absolute inset-0 opacity-20 pointer-events-none">
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] border border-white/10 rounded-full"></div>
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] border border-white/10 rounded-full"></div>
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[200px] h-[200px] border border-white/10 rounded-full"></div>
                        </div>

                        <div className="text-center z-10">
                            <div className="w-20 h-20 bg-blue-600 rounded-full mx-auto mb-6 flex items-center justify-center text-3xl shadow-[0_0_50px_rgba(37,99,235,0.4)]">🔍</div>
                            <h2 className="text-2xl font-bold mb-4">Select an entity to map its network</h2>
                            <p className="text-gray-500 max-w-sm mx-auto mb-8">Choose one of your recent checks to see how it links to other known scammer groups and phone numbers.</p>
                            <button className="bg-white text-black font-black py-3 px-8 rounded-xl hover:scale-105 transition-all">Start Mapping</button>
                        </div>
                    </div>

                    {/* Sidebar: Insights */}
                    <div className="space-y-6">
                        <div className="p-6 rounded-3xl bg-red-600/10 border border-red-600/20">
                            <h3 className="font-bold text-red-500 mb-2 uppercase text-xs">Active Clusters</h3>
                            <div className="text-3xl font-black">247</div>
                            <p className="text-[10px] text-red-400/60 font-medium mt-1 uppercase">Large scale scams detected this month</p>
                        </div>

                        <div className="p-8 rounded-3xl bg-white/5 border border-white/10">
                            <h3 className="font-black mb-6 uppercase text-sm">Recent Linkages</h3>
                            <div className="space-y-4">
                                <LinkItem type="Phone" id="017*** 521" reason="Same bKash" />
                                <LinkItem type="FB Page" id="Gadget Buzz" reason="Meta-data Match" />
                                <LinkItem type="Phone" id="019*** 882" reason="Draft Pattern" />
                            </div>
                        </div>

                        <div className="p-8 rounded-3xl bg-blue-600/10 border border-blue-600/20">
                            <h3 className="font-black mb-2 uppercase text-sm">How it works</h3>
                            <p className="text-xs text-blue-400/80 leading-relaxed">Our AI analyzes thousands of reports to find recurring identifiers. When multiple scams point to the same payment source or phone number, we map the entire network.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function LinkItem({ type, id, reason }: { type: string; id: string; reason: string }) {
    return (
        <div className="flex justify-between items-center py-3 border-b border-white/5 last:border-0">
            <div>
                <div className="text-[10px] font-bold text-gray-500 uppercase">{type}</div>
                <div className="text-sm font-bold text-white tracking-tight">{id}</div>
            </div>
            <div className="text-right">
                <span className="text-[9px] font-black bg-white/10 px-2 py-1 rounded text-white/70 uppercase">{reason}</span>
            </div>
        </div>
    );
}
