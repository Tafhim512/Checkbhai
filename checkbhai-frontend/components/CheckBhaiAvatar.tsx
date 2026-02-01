/**
 * CheckBhai Avatar Component
 * Friendly bot mascot with expressions based on risk level
 */

'use client';

import React from 'react';

interface CheckBhaiAvatarProps {
    riskLevel?: 'Low' | 'Medium' | 'High';
    size?: 'sm' | 'md' | 'lg';
}

export default function CheckBhaiAvatar({ riskLevel, size = 'md' }: CheckBhaiAvatarProps) {
    const sizeClasses = {
        sm: 'w-12 h-12',
        md: 'w-20 h-20',
        lg: 'w-32 h-32',
    };

    const getExpression = () => {
        switch (riskLevel) {
            case 'High':
                return '😰'; // Worried
            case 'Medium':
                return '🤔'; // Thinking
            case 'Low':
                return '😊'; // Happy
            default:
                return '🤖'; // Neutral bot
        }
    };

    return (
        <div className={`${sizeClasses[size]} flex items-center justify-center bg-gradient-to-br from-primary-400 to-primary-600 rounded-full shadow-lg animate-bounce-slow`}>
            <span className="text-4xl">{getExpression()}</span>
        </div>
    );
}
