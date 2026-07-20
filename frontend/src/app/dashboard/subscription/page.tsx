'use client';

import { useState } from 'react';

import { CreditCard, Check, ShieldCheck, Download } from 'lucide-react';

export default function Subscription() {
  const [transactions, setTransactions] = useState([
    { id: 'INV-2026-001', date: '2026-07-01', amount: 999, status: 'Success' }
  ]);


  return (
    <div className="space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Subscription Billing</h1>
        <p className="text-xs text-text-muted">Manage your Pro account parameters and invoices.</p>
      </div>

      {/* Current Plan Banner */}
      <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-6 border-l-4 border-l-primary-blue shadow-lg">
        <div className="flex gap-4 items-start">
          <div className="p-3 bg-blue-600/10 text-primary-blue rounded-md border border-primary-blue/20">
            <CreditCard className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-bold text-white text-base">You are on the Pro Plan</h3>
              <span className="text-[9px] font-bold bg-accent-emerald/20 text-accent-emerald px-1.5 py-0.5 rounded-sm">ACTIVE</span>
            </div>
            <p className="text-xs text-text-secondary mt-1">Valid until August 1, 2026. Auto-renewal amount: ₹499/month.</p>
          </div>
        </div>

        <div className="flex gap-3">
          <button className="h-9 px-4 rounded border border-border-subtle hover:bg-dark-bg text-xs font-semibold text-white transition-colors">
            Manage Billing
          </button>
          <button className="h-9 px-4 rounded hover:bg-red-500/10 text-xs font-semibold text-red-400 transition-colors">
            Cancel Plan
          </button>
        </div>
      </div>

      {/* Plan Comparisons */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Free */}
        <div className="p-6 bg-card-bg border border-border-strong rounded-lg opacity-60">
          <span className="text-xs font-bold text-text-muted tracking-wider block mb-1">FREE ACCESSIBLE</span>
          <h3 className="text-2xl font-extrabold text-white mb-4">₹0 <span className="text-xs text-text-muted font-normal">/ month</span></h3>
          <ul className="space-y-3 text-xs text-text-secondary mb-6">
            <li className="flex items-center gap-2">✓ Browse all upcoming IPOs</li>
            <li className="flex items-center gap-2">✓ Basic IPO profile metadata</li>
            <li className="flex items-center gap-2">✓ 3 AI analyses per month</li>
          </ul>
          <button disabled className="w-full py-2 rounded bg-dark-bg text-text-muted text-xs font-semibold cursor-not-allowed">
            Downgrade
          </button>
        </div>

        {/* Pro */}
        <div className="p-6 bg-card-bg border-2 border-primary-blue rounded-lg shadow-2xl relative">
          <span className="absolute -top-3 left-6 bg-accent-emerald text-white text-[9px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
            YOUR CURRENT PLAN
          </span>
          <span className="text-xs font-bold text-primary-blue tracking-wider block mb-1">PRO INVESTOR</span>
          <h3 className="text-2xl font-extrabold text-white mb-4">₹499 <span className="text-xs text-text-muted font-normal">/ month</span></h3>
          <ul className="space-y-3 text-xs text-text-secondary mb-6">
            <li className="flex items-center gap-2 font-semibold text-white"><Check className="w-4 h-4 text-accent-emerald" /> Unlimited AI analyses</li>
            <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> SWOT & Risk evaluation indexes</li>
            <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Contextual AI Chat</li>
            <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Telegram instant notification alerts</li>
          </ul>
          <button disabled className="w-full py-2 rounded bg-primary-blue/10 border border-primary-blue/30 text-primary-blue text-xs font-semibold">
            Active Plan
          </button>
        </div>

        {/* Enterprise */}
        <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between">
          <div>
            <span className="text-xs font-bold text-text-muted tracking-wider block mb-1">ENTERPRISE</span>
            <h3 className="text-2xl font-extrabold text-white mb-4">Custom</h3>
            <ul className="space-y-3 text-xs text-text-secondary mb-6">
              <li className="flex items-center gap-2">✓ All Pro features included</li>
              <li className="flex items-center gap-2">✓ Custom API data exports</li>
              <li className="flex items-center gap-2">✓ Dedicated analyst supervisor</li>
            </ul>
          </div>
          <button className="w-full py-2 rounded border border-border-subtle hover:bg-dark-bg text-white text-xs font-semibold transition-colors">
            Contact Support
          </button>
        </div>
      </div>

      {/* Transaction Table */}
      <div className="bg-card-bg border border-border-strong rounded-lg overflow-hidden">
        <div className="p-4 border-b border-border-strong bg-dark-bg/20">
          <h3 className="font-bold text-white text-base">Billing History</h3>
        </div>
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-border-strong bg-dark-bg/40 font-bold text-text-muted uppercase tracking-wider">
              <th className="p-4 pl-6">Invoice ID</th>
              <th className="p-4">Date</th>
              <th className="p-4">Amount</th>
              <th className="p-4">Status</th>
              <th className="p-4 pr-6 text-right">Receipt</th>
            </tr>
          </thead>
          <tbody className="text-text-secondary divide-y divide-border-strong/30">
            {transactions.slice(0, 3).map((tx) => (
              <tr key={tx.id} className="hover:bg-dark-bg/25">
                <td className="p-4 pl-6 font-bold text-white font-mono">{tx.id}</td>
                <td className="p-4 font-mono">{tx.date}</td>
                <td className="p-4 font-mono font-semibold text-white">₹{tx.amount}</td>
                <td className="p-4">
                  <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
                    tx.status === 'Success' ? 'bg-accent-emerald/10 text-accent-emerald' : 'bg-red-500/10 text-red-400'
                  }`}>
                    {tx.status.toUpperCase()}
                  </span>
                </td>
                <td className="p-4 pr-6 text-right">
                  <button className="p-1.5 rounded hover:bg-border-subtle text-text-muted hover:text-white transition-colors" title="Download PDF Invoice">
                    <Download className="w-3.5 h-3.5" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
