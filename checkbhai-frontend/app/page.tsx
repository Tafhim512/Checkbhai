/**
 * CheckBhai Home Page - Landing page with message input and scam detection
 */

'use client';

import { useState } from 'react';
import CheckBhaiAvatar from '@/components/CheckBhaiAvatar';
import RiskBadge from '@/components/RiskBadge';
import RedFlagsList from '@/components/RedFlagsList';
import api from '@/lib/api';

export default function Home() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleCheck = async () => {
    if (!message.trim()) {
      setError('Please enter a message to check');
      return;
    }

    if (message.length < 10) {
      setError('Message must be at least 10 characters long');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await api.checkMessage(message);
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to check message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-12 animate-fade-in">
        <div className="flex justify-center mb-6">
          <CheckBhaiAvatar size="lg" riskLevel={result?.risk_level} />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="gradient-text">CheckBhai</span>
        </h1>
        <p className="text-xl text-gray-600 mb-2">
          AI-Powered Scam Detection for Bangladesh 🇧🇩
        </p>
        <p className="text-gray-500">
          Protect yourself from scams in English, Bangla, or Banglish
        </p>
      </div>

      {/* Input Card */}
      <div className="card mb-8 animate-slide-up">
        <h2 className="text-2xl font-semibold mb-4">Check a Message</h2>
        <p className="text-gray-600 mb-4">
          Paste any suspicious message, job offer, investment opportunity, or sales pitch below.
        </p>

        <textarea
          className="input-field min-h-[150px] mb-4 resize-none"
          placeholder="আপনি selected হয়েছেন! Dubai job পাবেন, salary 80000 টাকা..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          disabled={loading}
        />

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        <button
          onClick={handleCheck}
          disabled={loading}
          className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Analyzing...
            </span>
          ) : (
            '🔍 Check for Scam'
          )}
        </button>
      </div>

      {/* Results Card */}
      {result && (
        <div className="card animate-fade-in">
          <div className="mb-6">
            <h2 className="text-2xl font-semibold mb-4">Analysis Results</h2>
            <RiskBadge level={result.risk_level} confidence={result.confidence} />
          </div>

          {/* Explanation */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-gray-700 leading-relaxed">{result.explanation}</p>
          </div>

          {/* Red Flags */}
          <RedFlagsList flags={result.red_flags} />

          {/* AI Details (Optional) */}
          {result.ai_prediction && (
            <div className="mt-6 pt-6 border-t border-gray-200 text-sm text-gray-600">
              <p>AI Prediction: <span className="font-medium">{result.ai_prediction}</span></p>
              {result.ai_confidence && (
                <p>AI Confidence: <span className="font-medium">{Math.round(result.ai_confidence * 100)}%</span></p>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="mt-6 flex gap-3">
            <button
              onClick={() => { setMessage(''); setResult(null); }}
              className="btn-secondary flex-1"
            >
              Check Another
            </button>
            {api.isLoggedIn() && (
              <button
                onClick={() => window.location.href = '/history'}
                className="btn-primary flex-1"
              >
                View History
              </button>
            )}
          </div>
        </div>
      )}

      {/* Features Section */}
      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-4xl mb-3">🤖</div>
          <h3 className="font-semibold mb-2">AI-Powered</h3>
          <p className="text-sm text-gray-600">Advanced machine learning detects scam patterns</p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-3">🌍</div>
          <h3 className="font-semibold mb-2">Multilingual</h3>
          <p className="text-sm text-gray-600">Works with English, Bangla & Banglish</p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-3">⚡</div>
          <h3 className="font-semibold mb-2">Instant Results</h3>
          <p className="text-sm text-gray-600">Get scam analysis in seconds</p>
        </div>
      </div>
    </div>
  );
}
