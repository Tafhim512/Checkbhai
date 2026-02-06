"use client";

import React, { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import api from "@/lib/api";

export default function ClaimPage() {
    const searchParams = useSearchParams();
    const router = useRouter();

    const entityId = searchParams.get('entityId');
    const identifier = searchParams.get('identifier');
    const type = searchParams.get('type');

    const [formData, setFormData] = useState({
        business_name: "",
        contact_email: "",
        verification_doc_url: "",
        message: ""
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        if (!entityId) {
            setError("No entity selected. Please start from an entity page.");
        }
    }, [entityId]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            if (!entityId) throw new Error("Entity ID missing");

            await api.claimEntity({
                entity_id: entityId,
                ...formData
            });
            setSuccess(true);
        } catch (err: any) {
            console.error("Claim failed:", err);
            setError(err.response?.data?.detail || "Failed to submit claim. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    if (success) {
        return (
            <div className="min-h-screen bg-[#0a0a0c] flex items-center justify-center p-6">
                <div className="max-w-md w-full bg-white/5 border border-white/10 rounded-[40px] p-8 text-center shadow-2xl">
                    <div className="text-6xl mb-6">✅</div>
                    <h1 className="text-2xl font-black text-white mb-4 uppercase tracking-tight">Claim Submitted</h1>
                    <p className="text-gray-400 mb-8 font-medium">
                        We have received your verification request. Our team will review your documents and contact you at <span className="text-white">{formData.contact_email}</span>.
                    </p>
                    <button
                        onClick={() => router.push(`/entities/${entityId}`)}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-xl w-full uppercase tracking-widest text-sm"
                    >
                        Back to Entity
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0a0a0c] text-white p-6 md:p-12 font-sans">
            <div className="max-w-2xl mx-auto">
                <div className="mb-8">
                    <button
                        onClick={() => router.back()}
                        className="text-gray-500 hover:text-white mb-4 text-xs font-bold uppercase tracking-widest transition-colors flex items-center gap-2"
                    >
                        ← Back
                    </button>
                    <h1 className="text-3xl md:text-4xl font-black uppercase tracking-tighter mb-2">Claim Business Profile</h1>
                    <p className="text-gray-400 font-medium">
                        Verify your ownership of <span className="text-blue-400 font-bold">{identifier}</span> ({type}).
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="bg-[#0f0f13] border border-white/5 rounded-[40px] p-8 md:p-10 shadow-xl space-y-6">
                    {error && (
                        <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-200 text-sm font-bold">
                            {error}
                        </div>
                    )}

                    <div className="space-y-2">
                        <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-2">Business / Owner Name</label>
                        <input
                            type="text"
                            required
                            className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-blue-500 transition-all text-white font-bold placeholder-white/20"
                            placeholder="Official Business Name"
                            value={formData.business_name}
                            onChange={(e) => setFormData({ ...formData, business_name: e.target.value })}
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-2">Contact Email</label>
                        <input
                            type="email"
                            required
                            className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-blue-500 transition-all text-white font-bold placeholder-white/20"
                            placeholder="owner@business.com"
                            value={formData.contact_email}
                            onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })}
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-2">Verification Document URL</label>
                        <input
                            type="url"
                            required
                            className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-blue-500 transition-all text-white font-bold placeholder-white/20"
                            placeholder="Link to Trade License / NID (Google Drive/Dropbox)"
                            value={formData.verification_doc_url}
                            onChange={(e) => setFormData({ ...formData, verification_doc_url: e.target.value })}
                        />
                        <p className="text-[10px] text-gray-600 pl-2">Provide a public link to your proof of ownership.</p>
                    </div>

                    <div className="space-y-2">
                        <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest ml-2">Message to Admin</label>
                        <textarea
                            required
                            rows={4}
                            className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-blue-500 transition-all text-white font-bold placeholder-white/20"
                            placeholder="Explain why this profile belongs to you and refute any false reports..."
                            value={formData.message}
                            onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading || !entityId}
                        className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-black py-4 rounded-2xl transition-all uppercase tracking-widest shadow-lg mt-4"
                    >
                        {loading ? "Submitting..." : "Submit Claim Request"}
                    </button>
                </form>
            </div>
        </div>
    );
}
