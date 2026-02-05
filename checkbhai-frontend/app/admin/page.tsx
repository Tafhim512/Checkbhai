/**
 * Admin Page - Minimal, Strong Admin Panel
 * - View all reports
 * - Mark report as Verified
 * - Remove spam reports
 * NO AI training, NO analytics bloat
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

interface Report {
    id: string;
    entity_id: string;
    platform: string;
    scam_type: string;
    amount_lost: number;
    description: string;
    status: string;
    created_at: string;
}

interface AdminStats {
    total_users: number;
    total_reports: number;
    verified_reports: number;
    pending_reports: number;
    total_entities: number;
    high_risk_entities: number;
}

export default function AdminPage() {
    const router = useRouter();
    const [stats, setStats] = useState<AdminStats | null>(null);
    const [reports, setReports] = useState<Report[]>([]);
    const [loading, setLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState<string>('pending');
    const [actionLoading, setActionLoading] = useState<string | null>(null);

    useEffect(() => {
        if (!api.isAdmin()) {
            router.push('/');
            return;
        }
        loadData();
    }, [statusFilter]);

    const loadData = async () => {
        setLoading(true);
        try {
            const [statsData, reportsData] = await Promise.all([
                api.getAdminStats(),
                api.getAdminReports(0, 50, statusFilter)
            ]);
            setStats(statsData);
            setReports(reportsData);
        } catch (error) {
            console.error('Failed to load admin data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleVerify = async (reportId: string) => {
        setActionLoading(reportId);
        try {
            await api.verifyReport(reportId);
            await loadData();
        } catch (error) {
            console.error('Failed to verify report:', error);
        } finally {
            setActionLoading(null);
        }
    };

    const handleMarkSpam = async (reportId: string) => {
        setActionLoading(reportId);
        try {
            await api.deleteReport(reportId);
            await loadData();
        } catch (error) {
            console.error('Failed to mark as spam:', error);
        } finally {
            setActionLoading(null);
        }
    };

    const formatScamType = (type: string) => {
        return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    };

    if (loading) {
        return (
            <div className="max-w-6xl mx-auto px-4 py-12">
                <div className="text-center">
                    <div className="animate-spin h-12 w-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading admin dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0a0a0c] text-white p-6">
            <div className="max-w-6xl mx-auto">
                <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

                {/* Stats Grid */}
                {stats && (
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-12">
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-2xl font-bold text-blue-400">{stats.total_users}</div>
                            <div className="text-xs text-gray-500 mt-1">Users</div>
                        </div>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-2xl font-bold text-white">{stats.total_reports}</div>
                            <div className="text-xs text-gray-500 mt-1">Total Reports</div>
                        </div>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-2xl font-bold text-yellow-400">{stats.pending_reports}</div>
                            <div className="text-xs text-gray-500 mt-1">Pending</div>
                        </div>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-2xl font-bold text-green-400">{stats.verified_reports}</div>
                            <div className="text-xs text-gray-500 mt-1">Verified</div>
                        </div>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-2xl font-bold text-white">{stats.total_entities}</div>
                            <div className="text-xs text-gray-500 mt-1">Entities</div>
                        </div>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-2xl font-bold text-red-400">{stats.high_risk_entities}</div>
                            <div className="text-xs text-gray-500 mt-1">High Risk</div>
                        </div>
                    </div>
                )}

                {/* Reports Section */}
                <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl font-bold">Reports</h2>
                        <select
                            className="bg-white/10 border border-white/10 rounded-lg px-4 py-2 text-sm"
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                        >
                            <option value="">All</option>
                            <option value="pending">Pending</option>
                            <option value="verified">Verified</option>
                            <option value="spam">Spam</option>
                        </select>
                    </div>

                    <div className="space-y-4">
                        {reports.length === 0 ? (
                            <div className="text-center py-12 text-gray-500">
                                No reports found
                            </div>
                        ) : (
                            reports.map((report) => (
                                <div key={report.id} className="bg-white/5 border border-white/10 rounded-xl p-4">
                                    <div className="flex justify-between items-start mb-3">
                                        <div>
                                            <span className={`text-xs font-bold uppercase px-2 py-1 rounded ${report.status === 'verified' ? 'bg-green-500/20 text-green-400' :
                                                    report.status === 'spam' ? 'bg-red-500/20 text-red-400' :
                                                        'bg-yellow-500/20 text-yellow-400'
                                                }`}>
                                                {report.status}
                                            </span>
                                            <span className="ml-2 text-xs text-gray-500">
                                                {formatScamType(report.scam_type)} on {report.platform}
                                            </span>
                                        </div>
                                        <span className="text-xs text-gray-500">
                                            {new Date(report.created_at).toLocaleDateString()}
                                        </span>
                                    </div>

                                    <p className="text-sm text-gray-300 mb-3 line-clamp-2">
                                        {report.description}
                                    </p>

                                    {report.amount_lost > 0 && (
                                        <p className="text-xs text-red-400 mb-3">
                                            Amount lost: ৳{report.amount_lost.toLocaleString()}
                                        </p>
                                    )}

                                    {report.status === 'pending' && (
                                        <div className="flex gap-2">
                                            <button
                                                onClick={() => handleVerify(report.id)}
                                                disabled={actionLoading === report.id}
                                                className="text-xs bg-green-600 hover:bg-green-700 px-3 py-1.5 rounded font-bold disabled:opacity-50"
                                            >
                                                {actionLoading === report.id ? '...' : '✓ Verify'}
                                            </button>
                                            <button
                                                onClick={() => handleMarkSpam(report.id)}
                                                disabled={actionLoading === report.id}
                                                className="text-xs bg-red-600 hover:bg-red-700 px-3 py-1.5 rounded font-bold disabled:opacity-50"
                                            >
                                                {actionLoading === report.id ? '...' : '✗ Spam'}
                                            </button>
                                        </div>
                                    )}
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
