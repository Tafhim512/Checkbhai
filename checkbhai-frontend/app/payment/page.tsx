/**
 * Payment Page - Handle Bkash, Rocket, Bank payments
 */

'use client';

import { useState } from 'react';
import api from '@/lib/api';

export default function PaymentPage() {
    const [method, setMethod] = useState<'bkash' | 'rocket' | 'bank'>('bkash');
    const [amount, setAmount] = useState(50);
    const [mobileNumber, setMobileNumber] = useState('');
    const [accountNumber, setAccountNumber] = useState('');
    const [bankName, setBankName] = useState('');
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState('');

    const packages = [
        { checks: 1, price: 50, popular: false },
        { checks: 10, price: 300, popular: true },
        { checks: 50, price: 1000, popular: false },
    ];

    const handlePayment = async () => {
        setError('');
        setSuccess(false);
        setLoading(true);

        try {
            const paymentData: any = {
                amount,
                method,
            };

            if (method === 'bkash' || method === 'rocket') {
                if (!mobileNumber || mobileNumber.length !== 11) {
                    throw new Error('Please enter a valid 11-digit mobile number');
                }
                paymentData.mobile_number = mobileNumber;
            } else if (method === 'bank') {
                if (!accountNumber || !bankName) {
                    throw new Error('Please enter account number and bank name');
                }
                paymentData.account_number = accountNumber;
                paymentData.bank_name = bankName;
            }

            await api.createPayment(paymentData);
            setSuccess(true);
            // Reset form
            setMobileNumber('');
            setAccountNumber('');
            setBankName('');
        } catch (err: any) {
            setError(err.message || 'Payment failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto px-4 py-12">
            <h1 className="text-3xl font-bold mb-8 text-center">Payment</h1>

            {/* Packages */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                {packages.map((pkg) => (
                    <div
                        key={pkg.checks}
                        className={`card cursor-pointer transition-all ${amount === pkg.price ? 'ring-4 ring-primary-500' : ''
                            } ${pkg.popular ? 'ring-2 ring-checkbhai-gold' : ''}`}
                        onClick={() => setAmount(pkg.price)}
                    >
                        {pkg.popular && (
                            <div className="bg-checkbhai-gold text-white text-xs font-bold px-3 py-1 rounded-full absolute -top-3 left-1/2 transform -translate-x-1/2">
                                POPULAR
                            </div>
                        )}
                        <div className="text-center">
                            <div className="text-4xl font-bold text-primary-600 mb-2">{pkg.checks}</div>
                            <div className="text-sm text-gray-600 mb-4">
                                {pkg.checks === 1 ? 'Check' : 'Checks'}
                            </div>
                            <div className="text-3xl font-bold mb-1">{pkg.price} ৳</div>
                            <div className="text-sm text-gray-500">
                                {pkg.checks > 1 && `${Math.round(pkg.price / pkg.checks)} ৳ per check`}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Payment Form */}
            <div className="card max-w-2xl mx-auto">
                <h2 className="text-2xl font-semibold mb-6">Select Payment Method</h2>

                {/* Method Selection */}
                <div className="grid grid-cols-3 gap-4 mb-6">
                    <button
                        onClick={() => setMethod('bkash')}
                        className={`p-4 rounded-lg border-2 transition-all ${method === 'bkash'
                                ? 'border-pink-500 bg-pink-50'
                                : 'border-gray-300 hover:border-pink-300'
                            }`}
                    >
                        <div className="text-2xl mb-1">📱</div>
                        <div className="font-semibold">Bkash</div>
                    </button>
                    <button
                        onClick={() => setMethod('rocket')}
                        className={`p-4 rounded-lg border-2 transition-all ${method === 'rocket'
                                ? 'border-purple-500 bg-purple-50'
                                : 'border-gray-300 hover:border-purple-300'
                            }`}
                    >
                        <div className="text-2xl mb-1">🚀</div>
                        <div className="font-semibold">Rocket</div>
                    </button>
                    <button
                        onClick={() => setMethod('bank')}
                        className={`p-4 rounded-lg border-2 transition-all ${method === 'bank'
                                ? 'border-blue-500 bg-blue-50'
                                : 'border-gray-300 hover:border-blue-300'
                            }`}
                    >
                        <div className="text-2xl mb-1">🏦</div>
                        <div className="font-semibold">Bank</div>
                    </button>
                </div>

                {/* Mobile Banking Fields */}
                {(method === 'bkash' || method === 'rocket') && (
                    <div className="mb-6">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Mobile Number
                        </label>
                        <input
                            type="tel"
                            maxLength={11}
                            placeholder="01XXXXXXXXX"
                            className="input-field"
                            value={mobileNumber}
                            onChange={(e) => setMobileNumber(e.target.value.replace(/\D/g, ''))}
                        />
                    </div>
                )}

                {/* Bank Transfer Fields */}
                {method === 'bank' && (
                    <>
                        <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Bank Name
                            </label>
                            <input
                                type="text"
                                placeholder="e.g., Dutch Bangla Bank"
                                className="input-field"
                                value={bankName}
                                onChange={(e) => setBankName(e.target.value)}
                            />
                        </div>
                        <div className="mb-6">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Account Number
                            </label>
                            <input
                                type="text"
                                placeholder="Account number"
                                className="input-field"
                                value={accountNumber}
                                onChange={(e) => setAccountNumber(e.target.value)}
                            />
                        </div>
                    </>
                )}

                {/* Amount Display */}
                <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-center">
                        <span className="font-semibold">Total Amount:</span>
                        <span className="text-2xl font-bold text-primary-600">{amount} ৳</span>
                    </div>
                </div>

                {/* Error/Success Messages */}
                {error && (
                    <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                        {error}
                    </div>
                )}
                {success && (
                    <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
                        ✅ Payment successful! Transaction ID has been sent to your email.
                    </div>
                )}

                {/* Submit Button */}
                <button
                    onClick={handlePayment}
                    disabled={loading}
                    className="btn-primary w-full disabled:opacity-50"
                >
                    {loading ? 'Processing...' : `Pay ${amount} ৳`}
                </button>

                <p className="text-xs text-gray-500 mt-4 text-center">
                    Note: This is a demo payment system. In production, real payment gateway integration would be required.
                </p>
            </div>
        </div>
    );
}
