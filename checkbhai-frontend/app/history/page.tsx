/**
 * History Page - User's message check history
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import RiskBadge from '@/components/RiskBadge';
import api from '@/lib/api';

export default function HistoryPage() {
    const router = useRouter();
    const [history, setHistory] = useState<any[]>([]);
    const [stats, setStats] = useState<any>(null);
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

    if (loading) {
        return (
            <div className="max-w-4xl mx-auto px-4 py-12">
                <div className="text-center">
                    <div className="animate-spin h-12 w-12 border-4 border-primary-600 border-t-transparent rounded-full mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading history...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto px-4 py-12">
            <h1 className="text-3xl font-bold mb-8">Your Check History</h1>

            {/* Stats Cards */}
            {stats && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    <div className="card text-center">
                        <div className="text-3xl font-bold text-primary-600">{stats.total_checks}</div>
                        <div className="text-sm text-gray-600">Total Checks</div>
                    </div>
                    <div className="card text-center">
                        <div className="text-3xl font-bold text-danger-600">{stats.high_risk_count}</div>
                        <div className="text-sm text-gray-600">High Risk</div>
                    </div>
                    <div className="card text-center">
                        <div className="text-3xl font-bold text-warning-600">{stats.medium_risk_count}</div>
                        <div className="text-sm text-gray-600">Medium Risk</div>
                    </div>
                    <div className="card text-center">
                        <div className="text-3xl font-bold text-primary-600">{stats.low_risk_count}</div>
                        <div className="text-sm text-gray-600">Low Risk</div>
                    </div>
                </div>
            )}

            {/* Filter */}
            <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Filter by Risk Level</label>
                <select
                    className="input-field max-w-xs"
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
                    <div className="card text-center py-12">
                        <p className="text-gray-600">No messages checked yet. <a href="/" className="text-primary-600 hover:underline">Check your first message</a></p>
                    </div>
                ) : (
                    history.map((item) => (
                        <div key={item.id} className="card">
                            <div className="flex justify-between items-start mb-3">
                                <RiskBadge level={item.risk_level} confidence={item.confidence} />
                                <span className="text-sm text-gray-500">
                                    {new Date(item.created_at).toLocaleDateString()} {new Date(item.created_at).toLocaleTimeString()}
                                </span>
                            </div>
                            <p className="text-gray-700 mb-3 line-clamp-2">{item.message_text}</p>
                            {item.explanation && (
                                <p className="text-sm text-gray-600 bg-gray-50 p-2 rounded">{item.explanation}</p>
                            )}
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
