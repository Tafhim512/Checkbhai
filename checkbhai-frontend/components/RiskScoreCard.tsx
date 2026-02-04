"use client";

import React from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

interface RiskScoreCardProps {
    score: number;
    trustLevel: string;
    type: string;
    identifier: string;
    scamProbability?: number;
}

const RiskScoreCard: React.FC<RiskScoreCardProps> = ({
    score,
    trustLevel,
    type,
    identifier,
    scamProbability
}) => {
    const getRiskColor = (s: number) => {
        if (s >= 70) return "text-red-500 border-red-500 bg-red-50";
        if (s >= 30) return "text-yellow-600 border-yellow-500 bg-yellow-50";
        return "text-green-500 border-green-500 bg-green-50";
    };

    const getRiskLabel = (s: number) => {
        if (s >= 70) return "High Risk / উচ্চ ঝুঁকি";
        if (s >= 30) return "Suspicious / সন্দেহজনক";
        return "Likely Safe / নিরাপদ";
    };

    const colors = getRiskColor(score);

    return (
        <div className={cn("p-6 rounded-2xl border-2 transition-all duration-300 shadow-lg", colors)}>
            <div className="flex justify-between items-start mb-4">
                <div>
                    <span className="text-sm font-medium opacity-70 uppercase tracking-wider">{type}</span>
                    <h2 className="text-2xl font-bold mt-1 truncate max-w-[200px]">{identifier}</h2>
                </div>
                <div className="flex flex-col items-end">
                    <div className="text-4xl font-extrabold">{score}%</div>
                    <div className="text-xs font-bold opacity-80 uppercase">Risk Score</div>
                </div>
            </div>

            <div className="mt-6 flex flex-col gap-3">
                <div className="flex items-center gap-2">
                    <div className={cn("w-3 h-3 rounded-full animate-pulse", score >= 70 ? "bg-red-500" : score >= 30 ? "bg-yellow-500" : "bg-green-500")}></div>
                    <span className="font-bold text-lg">{getRiskLabel(score)}</span>
                </div>

                {scamProbability !== undefined && (
                    <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
                        <div
                            className={cn("h-2.5 rounded-full transition-all duration-1000", score >= 70 ? "bg-red-600" : score >= 30 ? "bg-yellow-500" : "bg-green-500")}
                            style={{ width: `${score}%` }}
                        ></div>
                    </div>
                )}

                <p className="text-sm mt-2 opacity-90 leading-relaxed italic">
                    {score >= 70
                        ? "WARNING: This entity has been linked to potential fraud. Do not proceed with any transactions. / সাবধান: এই নম্বর/আইডিটি প্রতারণার সাথে জড়িত থাকতে পারে।"
                        : score >= 30
                            ? "CAUTION: Some suspicious patterns detected. Verify twice before sending money. / সতর্কতা: কিছু সন্দেহজনক প্যাটার্ন পাওয়া গেছে। লেনদেনের আগে যাচাই করুন।"
                            : "No major red flags found. However, always remain vigilant. / কোনো বড় ঝুঁকি পাওয়া যায়নি। তবুও সতর্ক থাকুন।"}
                </p>
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
