"use client";

import React, { useState } from "react";
import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ReportPage() {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        entity_id: "", // In real flow, this would be passed or searched
        identifier: "",
        type: "phone",
        scam_type: "fake_shop",
        amount_lost: 0,
        description: "",
        evidence: [] as { file_url: string; file_type: string }[]
    });
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);

    const handleSubmit = async () => {
        setLoading(true);
        try {
            // 1. First ensure entity exists
            const entityRes = await axios.get(`${API_BASE_URL}/entities/check`, {
                params: { type: formData.type, identifier: formData.identifier }
            });

            const entity_id = entityRes.data.id;

            // 2. Submit report
            await axios.post(`${API_BASE_URL}/reports`, {
                ...formData,
                entity_id
            }, {
                headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
            });

            setSuccess(true);
        } catch (err) {
            alert("Submission failed. Make sure you are logged in.");
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
                    <p className="text-gray-400 mb-8">Thank you for helping keep the community safe. Our team and AI are reviewing the evidence.</p>
                    <button onClick={() => window.location.href = "/"} className="bg-white text-black font-bold py-3 px-8 rounded-xl">Back to Home</button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0a0a0c] text-white p-6 md:p-12">
            <div className="max-w-2xl mx-auto">
                <h1 className="text-4xl font-black mb-2 tracking-tight">REPORT A SCAMER</h1>
                <p className="text-gray-500 font-bold mb-12 uppercase text-xs tracking-widest">Evidence-Based Verification Layer</p>

                <div className="bg-white/5 border border-white/10 rounded-3xl p-8 shadow-2xl">
                    {/* Progress Bar */}
                    <div className="flex gap-2 mb-12">
                        {[1, 2, 3].map((s) => (
                            <div key={s} className={`h-1.5 flex-1 rounded-full transition-all ${step >= s ? "bg-red-600" : "bg-white/10"}`}></div>
                        ))}
                    </div>

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
                                    <option value="phone">Phone / ফোন</option>
                                    <option value="fb_page">FB Page / ফেসবুক পেজ</option>
                                    <option value="bkash">bKash / বিকাশ</option>
                                    <option value="nagad">Nagad / নগদ</option>
                                </select>
                            </div>
                            <div className="flex flex-col gap-2">
                                <label className="text-xs font-bold text-gray-400 uppercase">Number or Link</label>
                                <input
                                    className="bg-white/10 border border-white/10 p-4 rounded-xl outline-none"
                                    placeholder="e.g. 017XXXXXXXX or URL"
                                    value={formData.identifier}
                                    onChange={(e) => setFormData({ ...formData, identifier: e.target.value })}
                                />
                            </div>
                            <button
                                onClick={() => setStep(2)}
                                disabled={!formData.identifier}
                                className="w-full bg-white text-black font-black py-4 rounded-xl mt-4"
                            >
                                NEXT STEP
                            </button>
                        </div>
                    )}

                    {step === 2 && (
                        <div className="space-y-6 animate-fade-in">
                            <h2 className="text-xl font-bold">Step 2: Incident Details</h2>
                            <div className="flex flex-col gap-2">
                                <label className="text-xs font-bold text-gray-400 uppercase">Scam Category</label>
                                <select
                                    className="bg-white/10 border border-white/10 p-4 rounded-xl outline-none"
                                    value={formData.scam_type}
                                    onChange={(e) => setFormData({ ...formData, scam_type: e.target.value })}
                                >
                                    <option value="fake_shop">Fake Shop / ফেক শপ</option>
                                    <option value="job_scam">Job Scam / চাকরির প্রতারণা</option>
                                    <option value="advance_fee">Advance Fee / অগ্রিম টাকা</option>
                                    <option value="investment">Investment Fraud / বিনিয়োগ প্রতারণা</option>
                                </select>
                            </div>
                            <div className="flex flex-col gap-2">
                                <label className="text-xs font-bold text-gray-400 uppercase">Amount Lost (BDT)</label>
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
                                    placeholder="Tell us the story..."
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                />
                            </div>
                            <div className="flex gap-4">
                                <button onClick={() => setStep(1)} className="flex-1 border border-white/10 font-bold py-4 rounded-xl">BACK</button>
                                <button onClick={() => setStep(3)} className="flex-1 bg-white text-black font-black py-4 rounded-xl">NEXT</button>
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="space-y-6 animate-fade-in">
                            <h2 className="text-xl font-bold">Step 3: Upload Evidence</h2>
                            <p className="text-sm text-gray-400">Please provide screenshots of the chat, payment receipt, or any other proof.</p>

                            <div className="border-2 border-dashed border-white/10 rounded-3xl p-12 text-center hover:bg-white/5 transition-colors cursor-pointer">
                                <div className="text-4xl mb-4">📸</div>
                                <p className="text-xs font-bold text-gray-500">CLICK TO UPLOAD SCREENSHOTS</p>
                                <p className="text-[10px] text-gray-600 mt-2">Maximum 5 images. JPG/PNG supported.</p>
                            </div>

                            <div className="p-4 bg-red-600/10 border border-red-600/30 rounded-xl">
                                <p className="text-[10px] text-red-400 font-bold leading-tight uppercase">Disclaimer: False reporting results in permanent ban / ভুল তথ্য দিলে আপনার আইডি আজীবন নিষিদ্ধ করা হবে।</p>
                            </div>

                            <div className="flex gap-4">
                                <button onClick={() => setStep(2)} className="flex-1 border border-white/10 font-bold py-4 rounded-xl">BACK</button>
                                <button
                                    onClick={handleSubmit}
                                    disabled={loading || !formData.description}
                                    className="flex-1 bg-red-600 hover:bg-red-700 text-white font-black py-4 rounded-xl"
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
