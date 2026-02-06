"use client";

import React from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

interface RiskScoreCardProps {
    riskStatus: string;  // Insufficient Data, Low Risk, Medium Risk, High Risk
    confidenceLevel: string;  // Low, Medium, High
    type: string;
    identifier: string;
    totalReports: number;
    scamReports: number;
    verifiedReports: number;
    lastReportedDate?: string | null;
}

const RiskScoreCard: React.FC<RiskScoreCardProps> = ({
    riskStatus,
    confidenceLevel,
    type,
    identifier,
    totalReports,
    scamReports,
    verifiedReports,
    lastReportedDate
}) => {
    const getRiskColor = (status: string) => {
        switch (status) {
            case "High Risk":
                return "text-red-500 border-red-500 bg-red-50";
            case "Medium Risk":
                return "text-yellow-600 border-yellow-500 bg-yellow-50";
            case "Low Risk":
                return "text-blue-500 border-blue-500 bg-blue-50";
            default:
                return "text-gray-500 border-gray-400 bg-gray-50";
        }
    };

    const getRiskLabel = (status: string) => {
        switch (status) {
            case "High Risk":
                return "High Risk / উচ্চ ঝুঁকি";
            case "Medium Risk":
                return "Medium Risk / মাঝারি ঝুঁকি";
            case "Low Risk":
                return "Low Risk / কম ঝুঁকি";
            default:
                return "Insufficient Data / অপর্যাপ্ত তথ্য";
        }
    };

    const getDotColor = (status: string) => {
        switch (status) {
            case "High Risk":
                return "bg-red-500";
            case "Medium Risk":
                return "bg-yellow-500";
            case "Low Risk":
                return "bg-blue-500";
            default:
                return "bg-gray-400";
        }
    };

    const formatDate = (dateString: string | null | undefined) => {
        if (!dateString) return "Never";
        const date = new Date(dateString);
        const now = new Date();
        const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
        if (diffDays === 0) return "Today";
        if (diffDays === 1) return "Yesterday";
        if (diffDays < 7) return `${diffDays} days ago`;
        return date.toLocaleDateString();
    };

    const colors = getRiskColor(riskStatus);

    return (
        <div className={cn("p-6 rounded-2xl border-2 transition-all duration-300 shadow-lg", colors)}>
            <div className="flex justify-between items-start mb-4">
                <div>
                    <span className="text-sm font-medium opacity-70 uppercase tracking-wider">{type}</span>
                    <h2 className="text-2xl font-bold mt-1 truncate max-w-[200px]">{identifier}</h2>
                </div>
                <div className="flex flex-col items-end">
                    <div className="text-sm font-bold opacity-80 uppercase">Confidence</div>
                    <div className="text-lg font-bold">{confidenceLevel}</div>
                </div>
            </div>

            <div className="mt-6 flex flex-col gap-3">
                <div className="flex items-center gap-2">
                    <div className={cn("w-3 h-3 rounded-full animate-pulse", getDotColor(riskStatus))}></div>
                    <span className="font-bold text-lg">{getRiskLabel(riskStatus)}</span>
                </div>

                {/* Community Stats */}
                <div className="grid grid-cols-3 gap-2 mt-4">
                    <div className="text-center p-2 bg-white/50 rounded-lg">
                        <div className="text-xl font-bold">{totalReports}</div>
                        <div className="text-[10px] opacity-70 uppercase">Reports</div>
                    </div>
                    <div className="text-center p-2 bg-white/50 rounded-lg">
                        <div className="text-xl font-bold">{verifiedReports}</div>
                        <div className="text-[10px] opacity-70 uppercase">Verified</div>
                    </div>
                    <div className="text-center p-2 bg-white/50 rounded-lg">
                        <div className="text-sm font-bold">{formatDate(lastReportedDate)}</div>
                        <div className="text-[10px] opacity-70 uppercase">Last Report</div>
                    </div>
                </div>

                {/* Warning - Always Shown */}
                <div className="mt-4 p-3 bg-yellow-100 border border-yellow-300 rounded-lg">
                    <p className="text-xs text-yellow-800 font-medium">
                        ⚠️ CheckBhai is community-powered. Always verify before payment.
                    </p>
                </div>
            </div>

            <div className="mt-6 flex justify-end">
                <button className="text-sm font-bold underline hover:opacity-70">
                    View Full History →
                </button>
            </div>
        </div>
    );
};

export default RiskScoreCard;
