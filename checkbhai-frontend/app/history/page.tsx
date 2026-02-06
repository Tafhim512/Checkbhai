/**
 * History Page - User's search history
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

interface HistoryItem {
    id: string;
    message_text: string;
    risk_level: string;
    confidence: number;
    red_flags: string[];
    explanation?: string;
    created_at: string;
}

interface UserStats {
    total_checks: number;
    high_risk_count: number;
    medium_risk_count: number;
    low_risk_count: number;
}

export default function HistoryPage() {
    const router = useRouter();
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [stats, setStats] = useState<UserStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<string>('');

    useEffect(() => {
        if (!api.isLoggedIn()) {
            router.push('/');
            return;
        }

        loadData();
    }, [filter]);

    const loadData = async () => {
        setLoading(true);
        try {
            const [historyData, statsData] = await Promise.all([
                api.getHistory(0, 20, filter || undefined),
                api.getUserStats()
            ]);
            setHistory(historyData);
            setStats(statsData);
        } catch (error) {
            console.error('Failed to load history:', error);
        } finally {
            setLoading(false);
        }
    };

    const getRiskColor = (level: string) => {
        switch (level) {
            case 'High':
                return 'bg-red-500/20 text-red-400 border-red-500/30';
            case 'Medium':
                return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
            default:
                return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-[#0a0a0c] flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin h-12 w-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto"></div>
                    <p className="mt-4 text-gray-400">Loading history...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0a0a0c] text-white p-6">
            <div className="max-w-5xl mx-auto">
                <h1 className="text-3xl font-bold mb-8">Your Check History</h1>

                {/* Stats Cards */}
                {stats && (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-3xl font-bold text-blue-400">{stats.total_checks}</div>
                            <div className="text-sm text-gray-500">Total Checks</div>
                        </div>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-3xl font-bold text-red-400">{stats.high_risk_count}</div>
                            <div className="text-sm text-gray-500">High Risk</div>
                        </div>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-3xl font-bold text-yellow-400">{stats.medium_risk_count}</div>
                            <div className="text-sm text-gray-500">Medium Risk</div>
                        </div>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                            <div className="text-3xl font-bold text-blue-400">{stats.low_risk_count}</div>
                            <div className="text-sm text-gray-500">Low Risk</div>
                        </div>
                    </div>
                )}

                {/* Filter */}
                <div className="mb-6">
                    <label className="block text-sm font-medium text-gray-400 mb-2">Filter by Risk Level</label>
                    <select
                        className="bg-white/10 border border-white/10 rounded-xl px-4 py-2 text-white"
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                    >
                        <option value="">All Messages</option>
                        <option value="High">High Risk Only</option>
                        <option value="Medium">Medium Risk Only</option>
                        <option value="Low">Low Risk Only</option>
                    </select>
                </div>

                {/* History List */}
                <div className="space-y-4">
                    {history.length === 0 ? (
                        <div className="bg-white/5 border border-white/10 rounded-xl p-12 text-center">
                            <p className="text-gray-500">
                                No messages checked yet.{' '}
                                <a href="/" className="text-blue-400 hover:underline">
                                    Check your first message
                                </a>
                            </p>
                        </div>
                    ) : (
                        history.map((item) => (
                            <div key={item.id} className="bg-white/5 border border-white/10 rounded-xl p-4">
                                <div className="flex justify-between items-start mb-3">
                                    <span className={`text-xs font-bold uppercase px-2 py-1 rounded border ${getRiskColor(item.risk_level)}`}>
                                        {item.risk_level} Risk
                                    </span>
                                    <span className="text-sm text-gray-500">
                                        {new Date(item.created_at).toLocaleDateString()}{' '}
                                        {new Date(item.created_at).toLocaleTimeString()}
                                    </span>
                                </div>
                                <p className="text-gray-300 mb-3 line-clamp-2">{item.message_text}</p>
                                {item.explanation && (
                                    <p className="text-sm text-gray-500 bg-white/5 p-2 rounded">{item.explanation}</p>
                                )}
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}
