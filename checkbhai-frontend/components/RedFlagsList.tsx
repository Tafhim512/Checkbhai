/**
 * Red Flags List Component
 * Displays detected red flags with icons
 */

import React from 'react';

interface RedFlagsListProps {
    flags: string[];
}

export default function RedFlagsList({ flags }: RedFlagsListProps) {
    if (!flags || flags.length === 0) {
        return null;
    }

    return (
        <div className="mt-4">
            <h3 className="font-semibold text-gray-700 mb-2">🚩 Red Flags Detected:</h3>
            <ul className="space-y-2">
                {flags.map((flag, index) => (
                    <li
                        key={index}
                        className="flex items-start gap-2 bg-red-50 border border-red-200 rounded-lg p-3 animate-slide-up"
                        style={{ animationDelay: `${index * 0.1}s` }}
                    >
                        <span className="text-red-600 mt-0.5">⚠️</span>
                        <span className="text-sm text-gray-700">{flag}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
}
