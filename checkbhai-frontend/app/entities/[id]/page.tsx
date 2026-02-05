"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/lib/api";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

interface EntityData {
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

interface ReportData {
    id: string;
    platform: string;
    scam_type: string;
    amount_lost: number;
    description: string;
    status: string;
    created_at: string;
}

export default function EntityDetailPage() {
    const params = useParams();
    const id = params.id as string;
    const router = useRouter();

    const [entity, setEntity] = useState<EntityData | null>(null);
    const [reports, setReports] = useState<ReportData[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        if (id) {
            loadData();
        }
    }, [id]);

    const loadData = async () => {
        setLoading(true);
        try {
            const [entityData, reportsData] = await Promise.all([
                api.getEntityDetails(id),
                api.getEntityReports(id)
            ]);
            setEntity(entityData);
            setReports(reportsData);
        } catch (err: any) {
            console.error("Failed to load entity details:", err);
            setError("Entity not found or server error.");
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (riskStatus: string) => {
        switch (riskStatus) {
            case "High Risk": return "text-red-500 bg-red-500/10 border-red-500/20";
            case "Medium Risk": return "text-yellow-500 bg-yellow-500/10 border-yellow-500/20";
            case "Low Risk": return "text-blue-500 bg-blue-500/10 border-blue-500/20";
            default: return "text-gray-500 bg-gray-500/10 border-gray-500/20";
        }
    };

    const formatDate = (dateString: string | null) => {
        if (!dateString) return "N/A";
        return new Date(dateString).toLocaleDateString(undefined, {
            year: 'numeric', month: 'long', day: 'numeric'
        });
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-[#0a0a0c] flex items-center justify-center">
                <div className="animate-spin h-10 w-10 border-4 border-blue-600 border-t-transparent rounded-full"></div>
            </div>
        );
    }

    if (error || !entity) {
        return (
            <div className="min-h-screen bg-[#0a0a0c] flex flex-col items-center justify-center p-6 text-center">
                <h1 className="text-4xl font-black text-white mb-4">404</h1>
                <p className="text-gray-500 mb-8">{error || "Entity not found"}</p>
                <button onClick={() => router.push('/')} className="bg-white text-black font-bold py-3 px-8 rounded-xl">Back to Safety</button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0a0a0c] text-white p-6 md:p-12">
            <div className="max-w-4xl mx-auto">
                {/* Entity Header */}
                <div className="bg-[#0f0f13] border border-white/5 rounded-[40px] p-8 md:p-12 shadow-2xl mb-8">
                    <div className="flex flex-col md:flex-row justify-between items-start gap-8">
                        <div>
                            <span className="text-[10px] font-black uppercase tracking-[0.3em] text-blue-500 mb-2 block">{entity.type} verification</span>
                            <h1 className="text-4xl md:text-6xl font-black tracking-tighter text-white mb-6 uppercase">{entity.identifier}</h1>
                            <div className={cn(
                                "inline-flex items-center gap-2 px-4 py-2 rounded-full border text-xs font-black uppercase tracking-widest",
                                getRiskColor(entity.risk_status)
                            )}>
                                <div className={cn("w-2 h-2 rounded-full",
                                    entity.risk_status === "High Risk" ? "bg-red-500" :
                                        entity.risk_status === "Medium Risk" ? "bg-yellow-500" : "bg-blue-500")}></div>
                                {entity.risk_status}
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4 w-full md:w-auto">
                            <div className="bg-white/5 p-6 rounded-3xl text-center border border-white/5">
                                <div className="text-3xl font-black text-white">{entity.total_reports}</div>
                                <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mt-1">Total Reports</div>
                            </div>
                            <div className="bg-white/5 p-6 rounded-3xl text-center border border-white/5">
                                <div className="text-sm font-black text-white">{entity.confidence_level}</div>
                                <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mt-1">Confidence</div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Reports List */}
                <div className="space-y-6">
                    <h2 className="text-2xl font-black uppercase tracking-tighter mb-8 ml-2">Community Evidence ({reports.length})</h2>

                    {reports.length === 0 ? (
                        <div className="bg-white/5 border border-white/5 rounded-3xl p-12 text-center">
                            <p className="text-gray-500 font-bold uppercase text-xs">No community reports found for this entity yet.</p>
                        </div>
                    ) : (
                        reports.map((report) => (
                            <div key={report.id} className="bg-[#0f0f13] border border-white/5 rounded-3xl p-8 hover:border-white/10 transition-all">
                                <div className="flex justify-between items-start mb-6">
                                    <div className="flex gap-3">
                                        <span className="bg-red-600/10 text-red-500 text-[10px] font-black px-3 py-1 rounded-full border border-red-500/10 uppercase tracking-widest">
                                            {report.scam_type.replace(/_/g, ' ')}
                                        </span>
                                        <span className="bg-white/5 text-gray-400 text-[10px] font-black px-3 py-1 rounded-full border border-white/10 uppercase tracking-widest">
                                            {report.platform}
                                        </span>
                                    </div>
                                    <span className="text-[10px] font-bold text-gray-600 uppercase tracking-widest">
                                        {formatDate(report.created_at)}
                                    </span>
                                </div>
                                <p className="text-gray-300 leading-relaxed font-medium mb-6">
                                    {report.description}
                                </p>
                                {report.amount_lost > 0 && (
                                    <div className="text-red-400 text-sm font-black uppercase tracking-tighter">
                                        Amount Lost: ৳{report.amount_lost.toLocaleString()}
                                    </div>
                                )}
                            </div>
                        ))
                    )}
                </div>

                <div className="mt-12 text-center">
                    <button
                        onClick={() => router.push(`/report?type=${entity.type}&identifier=${entity.identifier}&entity_id=${entity.id}`)}
                        className="bg-red-600 hover:bg-red-700 text-white font-black py-4 px-12 rounded-2xl shadow-xl transition-all uppercase tracking-widest text-sm"
                    >
                        🚩 File a New Report
                    </button>
                </div>
            </div>
        </div>
    );
}
