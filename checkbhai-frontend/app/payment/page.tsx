/**
 * Payment Page - Handle Bkash, Rocket, Bank payments
 */

'use client';

import { useState } from 'react';
import api from '@/lib/api';

export default function PaymentPage() {
    const [method, setMethod] = useState<'bkash' | 'nagad' | 'rocket' | 'bank'>('bkash');
    const [amount, setAmount] = useState(50);
    const [mobileNumber, setMobileNumber] = useState('');
    const [accountNumber, setAccountNumber] = useState('');
    const [bankName, setBankName] = useState('');
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState('');

    const packages = [
        { checks: 1, price: 50, popular: false, desc: "Single verification" },
        { checks: 10, price: 300, popular: true, desc: "Best for individuals" },
        { checks: 100, price: 2000, popular: false, desc: "Scale for Business" },
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

            if (method === 'bkash' || method === 'nagad' || method === 'rocket') {
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
            setMobileNumber('');
            setAccountNumber('');
            setBankName('');
        } catch (err: any) {
            setError(err.message || 'Payment failed. Please ensure the backend is connected.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#0a0a0c] text-white p-6 md:p-12">
            <div className="max-w-6xl mx-auto">
                <div className="text-center mb-16">
                    <h1 className="text-5xl font-black mb-4 tracking-tighter">GET MORE CHECKS</h1>
                    <p className="text-gray-500 font-bold uppercase text-xs tracking-[0.4em]">Scaling Trust for Everyone</p>
                </div>

                {/* Packages */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
                    {packages.map((pkg) => (
                        <div
                            key={pkg.checks}
                            className={`relative p-8 rounded-3xl border-4 transition-all cursor-pointer hover:scale-105 ${amount === pkg.price
                                ? 'bg-blue-600/10 border-blue-600 shadow-[0_0_30px_rgba(37,99,235,0.2)]'
                                : 'bg-white/5 border-white/10 hover:border-white/20'
                                }`}
                            onClick={() => setAmount(pkg.price)}
                        >
                            {pkg.popular && (
                                <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-[10px] font-black px-4 py-1.5 rounded-full shadow-lg">
                                    MOST POPULAR
                                </div>
                            )}
                            <div className="text-center">
                                <div className="text-6xl font-black text-white mb-2">{pkg.checks}</div>
                                <div className="text-sm font-bold text-gray-400 mb-6 uppercase tracking-widest">{pkg.checks === 1 ? 'Check' : 'Checks'}</div>
                                <div className="text-4xl font-black text-white mb-2">{pkg.price} ৳</div>
                                <p className="text-xs text-gray-500 font-medium mb-6">{pkg.desc}</p>
                                {pkg.checks > 1 && (
                                    <div className="text-[10px] font-bold text-blue-400 uppercase">Save {Math.round((pkg.checks * 50 - pkg.price) / (pkg.checks * 50) * 100)}% per check</div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Payment Form */}
                <div className="max-w-xl mx-auto bg-white/5 border border-white/10 p-10 rounded-[40px] shadow-2xl backdrop-blur-xl">
                    <h2 className="text-2xl font-black mb-10 text-center uppercase tracking-widest">Select Method</h2>

                    {/* Method Selection */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
                        <PaymentMethodButton
                            active={method === 'bkash'}
                            onClick={() => setMethod('bkash')}
                            color="border-pink-600 bg-pink-600/10"
                            label="bKash"
                            icon="📱"
                        />
                        <PaymentMethodButton
                            active={method === 'nagad'}
                            onClick={() => setMethod('nagad')}
                            color="border-orange-600 bg-orange-600/10"
                            label="Nagad"
                            icon="🔥"
                        />
                        <PaymentMethodButton
                            active={method === 'rocket'}
                            onClick={() => setMethod('rocket')}
                            color="border-purple-600 bg-purple-600/10"
                            label="Rocket"
                            icon="🚀"
                        />
                        <PaymentMethodButton
                            active={method === 'bank'}
                            onClick={() => setMethod('bank')}
                            color="border-blue-600 bg-blue-600/10"
                            label="Bank"
                            icon="🏦"
                        />
                    </div>

                    <div className="space-y-6">
                        {(method !== 'bank') && (
                            <div className="space-y-2">
                                <label className="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Your Mobile Number</label>
                                <input
                                    type="tel"
                                    maxLength={11}
                                    placeholder="01XXXXXXXXX"
                                    className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-blue-500 transition-all font-bold"
                                    value={mobileNumber}
                                    onChange={(e) => setMobileNumber(e.target.value.replace(/\D/g, ''))}
                                />
                            </div>
                        )}

                        {method === 'bank' && (
                            <>
                                <div className="space-y-2">
                                    <label className="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Bank Name</label>
                                    <input
                                        type="text"
                                        placeholder="e.g. Dutch Bangla Bank"
                                        className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-blue-500 transition-all font-bold"
                                        value={bankName}
                                        onChange={(e) => setBankName(e.target.value)}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-1">Account Number</label>
                                    <input
                                        type="text"
                                        placeholder="Account ID"
                                        className="w-full bg-white/5 border border-white/10 p-4 rounded-2xl outline-none focus:border-blue-500 transition-all font-bold"
                                        value={accountNumber}
                                        onChange={(e) => setAccountNumber(e.target.value)}
                                    />
                                </div>
                            </>
                        )}

                        <div className="bg-white/5 border border-white/5 p-6 rounded-2xl flex justify-between items-center">
                            <span className="font-bold text-gray-400 uppercase text-xs tracking-widest">Payable Amount</span>
                            <span className="text-3xl font-black text-white">{amount} ৳</span>
                        </div>

                        {error && (
                            <div className="p-4 bg-red-600/20 border border-red-600/40 rounded-2xl text-red-200 text-xs font-bold text-center">
                                {error}
                            </div>
                        )}
                        {success && (
                            <div className="p-4 bg-green-600/20 border border-green-600/40 rounded-2xl text-green-200 text-xs font-bold text-center">
                                ✅ Order placed! Check your email for next steps.
                            </div>
                        )}

                        <button
                            onClick={handlePayment}
                            disabled={loading}
                            className="w-full bg-white text-black font-black py-4 rounded-2xl text-lg hover:scale-[1.02] transition-all disabled:opacity-50"
                        >
                            {loading ? 'PROCESSING...' : `PAY ${amount} ৳`}
                        </button>

                        <p className="text-[9px] text-gray-600 font-bold uppercase text-center mt-6">
                            Secure Transaction Layer &bull; SSL Encryption Standard
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

function PaymentMethodButton({ active, onClick, color, label, icon }: { active: boolean; onClick: () => void; color: string; label: string; icon: string }) {
    return (
        <button
            onClick={onClick}
            className={`p-4 rounded-2xl border-2 transition-all flex flex-col items-center justify-center gap-2 ${active ? color : 'border-white/10 hover:bg-white/5'
                }`}
        >
            <div className="text-2xl">{icon}</div>
            <div className="text-[10px] font-black uppercase tracking-tighter">{label}</div>
        </button>
    );
}
