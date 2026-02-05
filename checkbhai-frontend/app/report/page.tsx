"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import api from "@/lib/api";

const SCAM_TYPES = [
    { value: "no_delivery", label: "No Delivery / পণ্য পাইনি" },
    { value: "fake_product", label: "Fake Product / নকল পণ্য" },
    { value: "advance_taken", label: "Advance Taken / অগ্রিম নিয়ে পালিয়েছে" },
    { value: "blocked_after_payment", label: "Blocked After Payment / পেমেন্টের পর ব্লক" },
    { value: "impersonation", label: "Impersonation / ছদ্মবেশ" },
    { value: "other", label: "Other / অন্যান্য" }
];

const PLATFORMS = [
    { value: "facebook", label: "Facebook / ফেসবুক" },
    { value: "whatsapp", label: "WhatsApp / হোয়াটসঅ্যাপ" },
    { value: "shop", label: "Shop / দোকান" },
    { value: "agent", label: "Agent / এজেন্ট" },
    { value: "other", label: "Other / অন্যান্য" }
];

const ENTITY_TYPES = [
    { value: "phone", label: "Phone / ফোন" },
    { value: "fb_page", label: "FB Page / ফেসবুক পেজ" },
    { value: "fb_profile", label: "FB Profile / ফেসবুক প্রোফাইল" },
    { value: "whatsapp", label: "WhatsApp / হোয়াটসঅ্যাপ" },
    { value: "shop", label: "Shop Name / দোকান" },
    { value: "agent", label: "Agent / এজেন্ট" },
    { value: "bkash", label: "bKash / বিকাশ" },
    { value: "nagad", label: "Nagad / নগদ" },
    { value: "rocket", label: "Rocket / রকেট" }
];

// Main component that uses useSearchParams - wrapped in Suspense by parent
function ReportForm() {
    const searchParams = useSearchParams();
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        entity_id: "",
        identifier: "",
        type: "phone",
        platform: "other",
        scam_type: "no_delivery",
        amount_lost: 0,
        description: "",
        evidence: [] as { file_url: string; file_type: string }[]
    });
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState("");

    // Pre-fill from URL params if coming from search result
    useEffect(() => {
        const type = searchParams.get("type");
        const identifier = searchParams.get("identifier");
        const entity_id = searchParams.get("entity_id");

        if (type && identifier) {
            setFormData(prev => ({
                ...prev,
                type: type,
                identifier: identifier,
                entity_id: entity_id || ""
            }));
        }
    }, [searchParams]);

    const handleSubmit = async () => {
        setLoading(true);
        setError("");
        console.log("[TRUTH LOOP] Starting report submission...");
        console.log("[TRUTH LOOP] Form data:", formData);

        try {
            let entity_id = formData.entity_id;

            // If no entity_id, first ensure entity exists
            if (!entity_id) {
                console.log("[TRUTH LOOP] No entity_id - fetching/creating entity first");
                const entityRes = await api.checkEntity(formData.type, formData.identifier);
                entity_id = entityRes.id;
                console.log("[TRUTH LOOP] Got entity_id:", entity_id);
            }

            // Submit report
            console.log("[TRUTH LOOP] Submitting report for entity:", entity_id);
            const reportRes = await api.submitReport({
                entity_id,
                platform: formData.platform,
                scam_type: formData.scam_type,
                amount_lost: formData.amount_lost,
                description: formData.description,
                evidence: formData.evidence
            });
            console.log("[TRUTH LOOP] Report submitted successfully:", reportRes);

            setSuccess(true);
        } catch (err: any) {
            console.error("[TRUTH LOOP] Report submission failed:", err);
            const detail = err.response?.data?.detail;
            setError(detail || "Submission failed. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    if (success) {
        return (
            <div className="min-h-screen bg-[#0a0a0c] flex items-center justify-center p-6">
                <div className="bg-green-500/10 border border-green-500/30 p-12 rounded-3xl text-center max-w-xl">
                    <div className="text-6xl mb-6">✅</div>
                    <h1 className="text-3xl font-black text-white mb-4">Report Submitted</h1>
                    <p className="text-gray-400 mb-8">
                        Thank you for helping keep the community safe. Your report has been added to this entity's record.
                    </p>
                    <button
                        onClick={() => window.location.href = "/"}
                        className="bg-white text-black font-bold py-3 px-8 rounded-xl"
                    >
                        Back to Home
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0a0a0c] text-white p-6 md:p-12">
            <div className="max-w-2xl mx-auto">
                <h1 className="text-4xl font-black mb-2 tracking-tight">REPORT A SCAM</h1>
                <p className="text-gray-500 font-bold mb-12 uppercase text-xs tracking-widest">
                    Community-Powered Trust Platform
                </p>

                <div className="bg-white/5 border border-white/10 rounded-3xl p-8 shadow-2xl">
                    {/* Progress Bar */}
                    <div className="flex gap-2 mb-12">
                        {[1, 2, 3].map((s) => (
                            <div
                                key={s}
                                className={`h-1.5 flex-1 rounded-full transition-all ${step >= s ? "bg-red-600" : "bg-white/10"}`}
                            ></div>
                        ))}
                    </div>

                    {error && (
                        <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-200 text-sm">
                            {error}
                        </div>
                    )}

                    {step === 1 && (
                        <div className="space-y-6 animate-fade-in">
                            <h2 className="text-xl font-bold">Step 1: Scammer Details</h2>

                            <div className="flex flex-col gap-2">
                                <label className="text-xs font-bold text-gray-400 uppercase">Identity Type</label>
                                <select
                                    className="bg-white/10 border border-white/10 p-4 rounded-xl outline-none"
                                    value={formData.type}
                                    onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                                >
                                    {ENTITY_TYPES.map(t => (
                                        <option key={t.value} value={t.value}>{t.label}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="flex flex-col gap-2">
                                <label className="text-xs font-bold text-gray-400 uppercase">Number, Name or Link</label>
                                <input
                                    className="bg-white/10 border border-white/10 p-4 rounded-xl outline-none"
                                    placeholder="e.g. 017XXXXXXXX or Facebook page URL"
                                    value={formData.identifier}
                                    onChange={(e) => setFormData({ ...formData, identifier: e.target.value })}
                                />
                            </div>

                            <button
                                onClick={() => setStep(2)}
                                disabled={!formData.identifier}
                                className="w-full bg-white text-black font-black py-4 rounded-xl mt-4 disabled:opacity-50"
                            >
                                NEXT STEP
                            </button>
                        </div>
                    )}

                    {step === 2 && (
                        <div className="space-y-6 animate-fade-in">
                            <h2 className="text-xl font-bold">Step 2: Incident Details</h2>

                            <div className="flex flex-col gap-2">
                                <label className="text-xs font-bold text-gray-400 uppercase">Platform</label>
                                <select
                                    className="bg-white/10 border border-white/10 p-4 rounded-xl outline-none"
                                    value={formData.platform}
                                    onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                                >
                                    {PLATFORMS.map(p => (
                                        <option key={p.value} value={p.value}>{p.label}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="flex flex-col gap-2">
                                <label className="text-xs font-bold text-gray-400 uppercase">Scam Category</label>
                                <select
                                    className="bg-white/10 border border-white/10 p-4 rounded-xl outline-none"
                                    value={formData.scam_type}
                                    onChange={(e) => setFormData({ ...formData, scam_type: e.target.value })}
                                >
                                    {SCAM_TYPES.map(t => (
                                        <option key={t.value} value={t.value}>{t.label}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="flex flex-col gap-2">
                                <label className="text-xs font-bold text-gray-400 uppercase">Amount Lost (BDT) - Optional</label>
                                <input
                                    type="number"
                                    className="bg-white/10 border border-white/10 p-4 rounded-xl outline-none"
                                    value={formData.amount_lost}
                                    onChange={(e) => setFormData({ ...formData, amount_lost: Number(e.target.value) })}
                                />
                            </div>

                            <div className="flex flex-col gap-2">
                                <label className="text-xs font-bold text-gray-400 uppercase">Describe What Happened</label>
                                <textarea
                                    className="bg-white/10 border border-white/10 p-4 rounded-xl outline-none min-h-[120px]"
                                    placeholder="Tell us the story... (minimum 20 characters)"
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                />
                            </div>

                            <div className="flex gap-4">
                                <button onClick={() => setStep(1)} className="flex-1 border border-white/10 font-bold py-4 rounded-xl">BACK</button>
                                <button
                                    onClick={() => setStep(3)}
                                    disabled={formData.description.length < 20}
                                    className="flex-1 bg-white text-black font-black py-4 rounded-xl disabled:opacity-50"
                                >
                                    NEXT
                                </button>
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="space-y-6 animate-fade-in">
                            <h2 className="text-xl font-bold">Step 3: Upload Evidence (Optional)</h2>
                            <p className="text-sm text-gray-400">
                                Screenshots help verify your report. You can skip this step now.
                            </p>

                            <div className="border-2 border-dashed border-white/10 rounded-3xl p-12 text-center hover:bg-white/5 transition-colors cursor-pointer">
                                <div className="text-4xl mb-4">📸</div>
                                <p className="text-xs font-bold text-gray-500">CLICK TO UPLOAD SCREENSHOTS</p>
                                <p className="text-[10px] text-gray-600 mt-2">Maximum 5 images. JPG/PNG supported.</p>
                            </div>

                            <div className="p-4 bg-red-600/10 border border-red-600/30 rounded-xl">
                                <p className="text-[10px] text-red-400 font-bold leading-tight uppercase">
                                    Disclaimer: False reporting may result in action against your account.
                                    <br />
                                    ভুল তথ্য দিলে আপনার বিরুদ্ধে ব্যবস্থা নেওয়া হতে পারে।
                                </p>
                            </div>

                            <div className="flex gap-4">
                                <button onClick={() => setStep(2)} className="flex-1 border border-white/10 font-bold py-4 rounded-xl">BACK</button>
                                <button
                                    onClick={handleSubmit}
                                    disabled={loading || formData.description.length < 20}
                                    className="flex-1 bg-red-600 hover:bg-red-700 text-white font-black py-4 rounded-xl disabled:opacity-50"
                                >
                                    {loading ? "SUBMITTING..." : "SUBMIT REPORT"}
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

// Loading fallback for Suspense
function ReportLoading() {
    return (
        <div className="min-h-screen bg-[#0a0a0c] flex items-center justify-center">
            <div className="text-center">
                <div className="animate-spin h-12 w-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto"></div>
                <p className="mt-4 text-gray-400">Loading report form...</p>
            </div>
        </div>
    );
}

// Default export wrapped in Suspense for useSearchParams
export default function ReportPage() {
    return (
        <Suspense fallback={<ReportLoading />}>
            <ReportForm />
        </Suspense>
    );
}
