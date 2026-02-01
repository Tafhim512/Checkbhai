/**
 * Risk Badge Component
 * Displays risk level with color coding
 */

import React from 'react';

interface RiskBadgeProps {
    level: 'Low' | 'Medium' | 'High';
    confidence?: number;
}

export default function RiskBadge({ level, confidence }: RiskBadgeProps) {
    const badgeStyles = {
        Low: 'badge-low',
        Medium: 'badge-medium',
        High: 'badge-high',
    };

    const icons = {
        Low: '✅',
        Medium: '⚠️',
        High: '🚨',
    };

    return (
        <div className="flex items-center gap-2">
            <span className={badgeStyles[level]}>
                <span className="mr-1">{icons[level]}</span>
                {level} Risk
            </span>
            {confidence !== undefined && (
                <span className="text-sm text-gray-600">
                    {Math.round(confidence * 100)}% confident
                </span>
            )}
        </div>
    );
}
