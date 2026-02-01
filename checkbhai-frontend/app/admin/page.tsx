/**
 * Admin Page - Platform statistics and AI retraining
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import RiskBadge from '@/components/RiskBadge';
import api from '@/lib/api';

export default function AdminPage() {
    const router = useRouter();
    const [stats, setStats] = useState<any>(null);
    const [messages, setMessages] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [retrainText, setRetrainText] = useState('');
    const [retrainLabel, setRetrainLabel] = useState<'Scam' | 'Legit'>('Scam');
    const [retrainLoading, setRetrainLoading] = useState(false);
    const [retrainSuccess, setRetrainSuccess] = useState('');

    useEffect(() => {
        if (!api.isAdmin()) {
            router.push('/');
            return;
        }
        loadData();
    }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const [statsData, messagesData] = await Promise.all([
                api.getAdminStats(),
                api.getAllMessages(0, 20)
            ]);
            setStats(statsData);
            setMessages(messagesData);
        } catch (error) {
            console.error('Failed to load admin data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleRetrain = async () => {
        if (!retrainText.trim()) return;

        setRetrainLoading(true);
        setRetrainSuccess('');
        try {
            await api.retrainModel([
                { text: retrainText, label: retrainLabel }
            ]);
            setRetrainSuccess('✅ Model retrained successfully!');
            setRetrainText('');
            setTimeout(() => setRetrainSuccess(''), 3000);
        } catch (error) {
            console.error('Failed to retrain model:', error);
        } finally {
            setRetrainLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="max-w-6xl mx-auto px-4 py-12">
                <div className="text-center">
                    <div className="animate-spin h-12 w-12 border-4 border-primary-600 border-t-transparent rounded-full mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading admin dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-6xl mx-auto px-4 py-12">
            <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

            {/* Stats Grid */}
            {stats && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
                    <div className="card text-center">
                        <div className="text-4xl font-bold text-primary-600">{stats.total_users}</div>
                        <div className="text-sm text-gray-600 mt-2">Total Users</div>
                    </div>
                    <div className="card text-center">
                        <div className="text-4xl font-bold text-blue-600">{stats.total_checks}</div>
                        <div className="text-sm text-gray-600 mt-2">Total Checks</div>
                    </div>
                    <div className="card text-center">
                        <div className="text-4xl font-bold text-danger-600">{stats.total_scams_detected}</div>
                        <div className="text-sm text-gray-600 mt-2">Scams Detected</div>
                    </div>
                    <div className="card text-center">
                        <div className="text-4xl font-bold text-checkbhai-gold">{stats.scam_percentage.toFixed(1)}%</div>
                        <div className="text-sm text-gray-600 mt-2">Scam Rate</div>
                    </div>
                </div>
            )}

            {/* AI Retraining Section */}
            <div className="card mb-8">
                <h2 className="text-2xl font-semibold mb-4">🤖 AI Model Retraining (Human-in-Loop)</h2>
                <p className="text-gray-600 mb-4">
                    Add new training examples to improve the AI model's accuracy
                </p>

                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Message Text</label>
                    <textarea
                        className="input-field min-h-[100px]"
                        placeholder="Enter a scam or legitimate message example..."
                        value={retrainText}
                        onChange={(e) => setRetrainText(e.target.value)}
                    />
                </div>

                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Label</label>
                    <div className="flex gap-4">
                        <label className="flex items-center">
                            <input
                                type="radio"
                                name="label"
                                value="Scam"
                                checked={retrainLabel === 'Scam'}
                                onChange={() => setRetrainLabel('Scam')}
                                className="mr-2"
                            />
                            <span>Scam</span>
                        </label>
                        <label className="flex items-center">
                            <input
                                type="radio"
                                name="label"
                                value="Legit"
                                checked={retrainLabel === 'Legit'}
                                onChange={() => setRetrainLabel('Legit')}
                                className="mr-2"
                            />
                            <span>Legitimate</span>
                        </label>
                    </div>
                </div>

                {retrainSuccess && (
                    <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700">
                        {retrainSuccess}
                    </div>
                )}

                <button
                    onClick={handleRetrain}
                    disabled={retrainLoading || !retrainText.trim()}
                    className="btn-primary disabled:opacity-50"
                >
                    {retrainLoading ? 'Retraining...' : 'Add to Training & Retrain Model'}
                </button>
            </div>

            {/* Recent Messages */}
            <div className="card">
                <h2 className="text-2xl font-semibold mb-6">Recent Messages</h2>
                <div className="space-y-4">
                    {messages.map((msg) => (
                        <div key={msg.id} className="border-b border-gray-200 pb-4 last:border-0">
                            <div className="flex justify-between items-start mb-2">
                                <RiskBadge level={msg.risk_level} confidence={msg.confidence} />
                                <span className="text-xs text-gray-500">
                                    {new Date(msg.created_at).toLocaleString()}
                                </span>
                            </div>
                            <p className="text-sm text-gray-700">{msg.message_text}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
