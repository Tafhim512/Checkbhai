"use client";

import React, { useState } from "react";
import axios from "axios";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const EntitySearch: React.FC = () => {
    const [identifier, setIdentifier] = useState("");
    const [type, setType] = useState("phone");
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState("");

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!identifier) return;

        setLoading(true);
        setError("");
        setResult(null);

        try {
            const response = await axios.get(`${API_BASE_URL}/entities/check`, {
                params: { type, identifier }
            });
            setResult(response.data);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Something went wrong. Please try again.");
        } finally {
            setLoading(false);
        }
    };

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
                        <option className="text-black" value="bkash">bKash / বিকাশ</option>
                        <option className="text-black" value="nagad">Nagad / নগদ</option>
                        <option className="text-black" value="website">Website / ওয়েবসাইট</option>
                    </select>
                    <input
                        type="text"
                        value={identifier}
                        onChange={(e) => setIdentifier(e.target.value)}
                        placeholder="Search number or URL... / সার্চ করুন..."
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

            {result && (
                <div className="mt-8 transform transition-all duration-500 animate-fade-in-up">
                    <div className={cn(
                        "p-8 rounded-3xl border-4 shadow-2xl backdrop-blur-xl",
                        result.risk_score >= 70 ? "bg-red-500/10 border-red-500/30" : result.risk_score >= 30 ? "bg-yellow-500/10 border-yellow-500/30" : "bg-green-500/10 border-green-500/30"
                    )}>
                        <div className="flex justify-between items-start">
                            <div>
                                <span className="text-xs font-bold uppercase tracking-widest text-white/60">{result.type}</span>
                                <h3 className="text-3xl font-black text-white mt-1">{result.identifier}</h3>
                            </div>
                            <div className="text-right">
                                <div className="text-4xl font-black text-white">{result.risk_score}%</div>
                                <div className="text-[10px] font-bold text-white/60 tracking-tighter uppercase">Scam Probability</div>
                            </div>
                        </div>

                        <div className="mt-8 flex items-center gap-3">
                            <div className={cn(
                                "w-4 h-4 rounded-full shadow-[0_0_15px_rgba(255,255,255,0.5)]",
                                result.risk_score >= 70 ? "bg-red-500" : result.risk_score >= 30 ? "bg-yellow-500" : "bg-green-500"
                            )}></div>
                            <span className="text-xl font-black text-white tracking-tight">
                                {result.risk_score >= 70 ? "HIGH RISK / উচ্চ ঝুঁকি" : result.risk_score >= 30 ? "SUSPICIOUS / সন্দেহজনক" : "SAFE / নিরাপদ"}
                            </span>
                        </div>

                        <p className="mt-4 text-white/80 leading-relaxed text-sm font-medium">
                            {result.risk_score >= 70
                                ? "This identity is strongly linked to scam activities. Avoid transactions at all costs. / এই নম্বর/আইডিটি প্রতারণার সাথে জড়িত। লেনদেন করবেন না।"
                                : result.risk_score >= 30
                                    ? "Some suspicious reports found. Verify identity before sending any money. / কিছু সন্দেহজনক তথ্য পাওয়া গেছে। টাকা পাঠানোর আগে যাচাই করুন।"
                                    : "Verified as safe for now. Continue with standard caution. / বর্তমানে নিরাপদ বলে মনে হচ্ছে। সাধারণ সতর্কতা বজায় রাখুন।"}
                        </p>

                        <div className="mt-8 flex gap-4">
                            <button className="flex-1 bg-white/10 hover:bg-white/20 text-white font-bold py-3 rounded-xl transition-all border border-white/10 text-sm">
                                Full Report
                            </button>
                            <button className="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-xl transition-all shadow-lg text-sm">
                                Report Scam
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default EntitySearch;
