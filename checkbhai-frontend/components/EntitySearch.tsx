"use client";

import React, { useState } from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

import api from "@/lib/api";

interface EntityResult {
    id: string;
    type: string;
    identifier: string;
    risk_status: string;
    confidence_level: string;
    total_reports: number;
    scam_reports: number;
    verified_reports: number;
    last_reported_date: string | null;
}

interface MessageResult {
    risk_level: string;
    red_flags: string[];
    explanation_en?: string;
    explanation_bn?: string;
}

const EntitySearch: React.FC = () => {
    const [identifier, setIdentifier] = useState("");
    const [type, setType] = useState("phone");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<EntityResult | MessageResult | null>(null);
    const [resultType, setResultType] = useState<"entity" | "message">("entity");
    const [error, setError] = useState("");

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!identifier) return;

        // Auto-detect if it's a message if the user pasted a long text
        let currentType = type;
        if (identifier.length > 30 && currentType !== "message" && !identifier.includes("/") && !identifier.includes(".")) {
            currentType = "message";
            setType("message");
        }

        setLoading(true);
        setError("");
        setResult(null);

        try {
            if (currentType === "message") {
                const data = await api.checkMessage(identifier);
                console.log("[TRUTH LOOP] Message check response:", data);
                setResult(data);
                setResultType("message");
            } else {
                const data = await api.checkEntity(type, identifier);
                console.log("[TRUTH LOOP] Entity check response:", data);
                console.log("[TRUTH LOOP] risk_status:", data.risk_status);
                console.log("[TRUTH LOOP] total_reports:", data.total_reports);
                console.log("[TRUTH LOOP] scam_reports:", data.scam_reports);
                console.log("[TRUTH LOOP] verified_reports:", data.verified_reports);
                setResult(data);
                setResultType("entity");
            }
        } catch (err: any) {
            console.error("Search API Error:", err);
            const detail = err.response?.data?.detail || err.response?.data?.error;
            if (detail) {
                setError(`Server Error: ${detail}`);
            } else if (err.code === "ERR_NETWORK" || err.message === "Network Error") {
                setError(`Connection Error: The frontend cannot reach the backend. Please check your Render URL/Status.`);
            } else {
                setError(`Error: ${err.message}`);
            }
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (riskStatus: string) => {
        switch (riskStatus) {
            case "High Risk":
                return "bg-red-500/10 border-red-500/30";
            case "Medium Risk":
                return "bg-yellow-500/10 border-yellow-500/30";
            case "Low Risk":
                return "bg-blue-500/10 border-blue-500/30";
            default: // Insufficient Data
                return "bg-gray-500/10 border-gray-500/30";
        }
    };

    const getRiskDot = (riskStatus: string) => {
        switch (riskStatus) {
            case "High Risk":
                return "bg-red-500";
            case "Medium Risk":
                return "bg-yellow-500";
            case "Low Risk":
                return "bg-blue-500";
            default:
                return "bg-gray-500";
        }
    };

    const getRiskLabel = (riskStatus: string) => {
        switch (riskStatus) {
            case "High Risk":
                return "HIGH RISK / উচ্চ ঝুঁকি";
            case "Medium Risk":
                return "MEDIUM RISK / মাঝারি ঝুঁকি";
            case "Low Risk":
                return "LOW RISK / কম ঝুঁকি";
            default:
                return "INSUFFICIENT DATA / অপর্যাপ্ত তথ্য";
        }
    };

    const formatDate = (dateString: string | null) => {
        if (!dateString) return "Never";
        const date = new Date(dateString);
        const now = new Date();
        const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
        if (diffDays === 0) return "Today";
        if (diffDays === 1) return "Yesterday";
        if (diffDays < 7) return `${diffDays} days ago`;
        return date.toLocaleDateString();
    };

    const entityResult = resultType === "entity" ? result as EntityResult : null;
    const messageResult = resultType === "message" ? result as MessageResult : null;

    return (
        <div className="w-full max-w-2xl mx-auto">
            <form onSubmit={handleSearch} className="flex flex-col gap-4">
                <div className="flex gap-2 p-1 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 shadow-2xl">
                    <select
                        value={type}
                        onChange={(e) => setType(e.target.value)}
                        className="bg-transparent text-white font-medium p-3 outline-none border-none cursor-pointer hover:bg-white/5 rounded-xl transition-colors"
                    >
                        <option className="text-black" value="phone">Phone / ফোন</option>
                        <option className="text-black" value="fb_page">FB Page / ফেসবুক পেজ</option>
                        <option className="text-black" value="fb_profile">FB Profile / ফেসবুক প্রোফাইল</option>
                        <option className="text-black" value="whatsapp">WhatsApp / হোয়াটসঅ্যাপ</option>
                        <option className="text-black" value="shop">Shop Name / দোকান</option>
                        <option className="text-black" value="agent">Agent / এজেন্ট</option>
                        <option className="text-black" value="bkash">bKash / বিকাশ</option>
                        <option className="text-black" value="nagad">Nagad / নগদ</option>
                        <option className="text-black" value="rocket">Rocket / রকেট</option>
                        <option className="text-black" value="message">Full Message / পূর্ণ বার্তা</option>
                    </select>
                    <input
                        type="text"
                        value={identifier}
                        onChange={(e) => setIdentifier(e.target.value)}
                        placeholder={type === "message" ? "Paste the suspicious message here..." : "Search number, name or URL... / সার্চ করুন..."}
                        className="flex-1 bg-transparent p-3 text-white placeholder-white/50 outline-none border-none text-lg"
                    />
                    <button
                        type="submit"
                        disabled={loading}
                        className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white font-bold py-3 px-8 rounded-xl transition-all shadow-lg active:scale-95"
                    >
                        {loading ? "Checking..." : "CHECK"}
                    </button>
                </div>
            </form>

            {error && (
                <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm animate-shake">
                    {error}
                </div>
            )}

            {entityResult && (
                <div className="mt-8 transform transition-all duration-500 animate-fade-in-up">
                    <div className={cn(
                        "p-8 rounded-3xl border-4 shadow-2xl backdrop-blur-xl",
                        getRiskColor(entityResult.risk_status)
                    )}>
                        {/* Header */}
                        <div className="flex justify-between items-start">
                            <div>
                                <span className="text-xs font-bold uppercase tracking-widest text-white/60">{entityResult.type}</span>
                                <h3 className="text-3xl font-black text-white mt-1">{entityResult.identifier}</h3>
                            </div>
                            <div className="text-right">
                                <div className="text-xs font-bold uppercase text-white/60 tracking-tight">Confidence</div>
                                <div className="text-lg font-bold text-white">{entityResult.confidence_level}</div>
                            </div>
                        </div>

                        {/* Risk Status Badge */}
                        <div className="mt-8 flex items-center gap-3">
                            <div className={cn(
                                "w-4 h-4 rounded-full shadow-[0_0_15px_rgba(255,255,255,0.5)]",
                                getRiskDot(entityResult.risk_status)
                            )}></div>
                            <span className="text-xl font-black text-white tracking-tight">
                                {getRiskLabel(entityResult.risk_status)}
                            </span>
                        </div>

                        {/* Community Stats */}
                        <div className="mt-6 grid grid-cols-3 gap-4">
                            <div className="bg-white/5 rounded-xl p-4 text-center">
                                <div className="text-2xl font-black text-white">{entityResult.total_reports}</div>
                                <div className="text-[10px] text-white/60 uppercase font-bold">Total Reports</div>
                            </div>
                            <div className="bg-white/5 rounded-xl p-4 text-center">
                                <div className="text-2xl font-black text-white">{entityResult.verified_reports}</div>
                                <div className="text-[10px] text-white/60 uppercase font-bold">Verified</div>
                            </div>
                            <div className="bg-white/5 rounded-xl p-4 text-center">
                                <div className="text-sm font-black text-white">{formatDate(entityResult.last_reported_date)}</div>
                                <div className="text-[10px] text-white/60 uppercase font-bold">Last Report</div>
                            </div>
                        </div>

                        {/* Warning Banner - ALWAYS SHOWN */}
                        <div className="mt-6 p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-xl">
                            <p className="text-xs text-yellow-200 font-medium">
                                ⚠️ CheckBhai is community-powered. Always verify before payment.
                                <br />
                                <span className="text-yellow-300/80">চেকভাই সম্প্রদায়-চালিত। পেমেন্টের আগে সর্বদা যাচাই করুন।</span>
                            </p>
                        </div>

                        {/* Action Buttons */}
                        <div className="mt-8 flex flex-col md:flex-row gap-4">
                            <button
                                onClick={() => window.location.href = `/report?type=${entityResult.type}&identifier=${entityResult.identifier}&entity_id=${entityResult.id}`}
                                className="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-xl transition-all shadow-lg text-xs uppercase tracking-widest"
                            >
                                🚩 Report Scam
                            </button>
                            <button
                                onClick={() => window.location.href = `/entities/${entityResult.id}`}
                                className="flex-1 bg-white/5 hover:bg-white/10 text-white font-bold py-3 rounded-xl transition-all border border-white/5 text-xs uppercase tracking-widest"
                            >
                                🔍 View All Proof
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {messageResult && (
                <div className="mt-8 transform transition-all duration-500 animate-fade-in-up">
                    <div className={cn(
                        "p-8 rounded-3xl border-4 shadow-2xl backdrop-blur-xl",
                        messageResult.risk_level === "High" ? "bg-red-500/10 border-red-500/30" :
                            messageResult.risk_level === "Medium" ? "bg-yellow-500/10 border-yellow-500/30" :
                                "bg-blue-500/10 border-blue-500/30"
                    )}>
                        <div className="flex items-center gap-3 mb-6">
                            <div className={cn(
                                "w-4 h-4 rounded-full shadow-[0_0_15px_rgba(255,255,255,0.5)]",
                                messageResult.risk_level === "High" ? "bg-red-500" :
                                    messageResult.risk_level === "Medium" ? "bg-yellow-500" : "bg-blue-500"
                            )}></div>
                            <span className="text-xl font-black text-white tracking-tight">
                                {messageResult.risk_level === "High" ? "HIGH RISK / উচ্চ ঝুঁকি" :
                                    messageResult.risk_level === "Medium" ? "MEDIUM RISK / মাঝারি ঝুঁকি" :
                                        "LOW RISK / কম ঝুঁকি"}
                            </span>
                        </div>

                        {/* AI Explanation */}
                        {(messageResult.explanation_en || messageResult.explanation_bn) && (
                            <div className="space-y-4">
                                {messageResult.explanation_en && (
                                    <p className="text-white/90 leading-relaxed text-sm font-medium border-l-2 border-white/20 pl-4 italic">
                                        {messageResult.explanation_en}
                                    </p>
                                )}
                                {messageResult.explanation_bn && (
                                    <p className="text-white/90 leading-relaxed text-sm font-medium border-l-2 border-white/20 pl-4 italic">
                                        {messageResult.explanation_bn}
                                    </p>
                                )}
                            </div>
                        )}

                        {/* Red Flags List */}
                        {messageResult.red_flags && messageResult.red_flags.length > 0 && (
                            <div className="mt-6">
                                <h4 className="text-[10px] font-bold text-red-400 uppercase tracking-widest mb-3">Red Flags Detected</h4>
                                <div className="flex flex-wrap gap-2">
                                    {messageResult.red_flags.map((flag: string, i: number) => (
                                        <span key={i} className="text-[10px] bg-red-500/20 text-red-200 px-2 py-1 rounded border border-red-500/20">
                                            🚩 {flag}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Warning Banner */}
                        <div className="mt-6 p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-xl">
                            <p className="text-xs text-yellow-200 font-medium">
                                ⚠️ CheckBhai is community-powered. Always verify before payment.
                            </p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default EntitySearch;
