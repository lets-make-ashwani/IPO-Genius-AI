'use client';

import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import Link from 'next/link';
import { useState } from 'react';
import { Sparkles, Check, HelpCircle } from 'lucide-react';

export default function Pricing() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');

  const faqs = [
    { q: 'How does the billing cycle work?', a: 'Subscriptions are billed on a monthly or yearly cycle depending on your choice. Yearly subscriptions enjoy a 20% discount.' },
    { q: 'Can I change plans later?', a: 'Yes. You can upgrade, downgrade, or cancel your Pro Plan subscription at any time directly from the billing history tab in settings.' },
    { q: 'What payment options do you support?', a: 'We accept Razorpay integration including credit cards, debit cards, UPI options, net banking, and wallets across India.' }
  ];

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col pt-16">
      <Navbar />

      <section className="py-20 px-6 text-center max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-6">
          Simple, Transparent Pricing
        </h1>
        <p className="text-lg text-text-secondary mb-8">
          Choose the right plan to accelerate your investment research.
        </p>

        <div className="flex items-center justify-center gap-3 mb-16">
          <span className={`text-sm ${billingCycle === 'monthly' ? 'text-white font-bold' : 'text-text-muted'}`}>Monthly</span>
          <button
            onClick={() => setBillingCycle(prev => prev === 'monthly' ? 'yearly' : 'monthly')}
            className="w-12 h-6 rounded-full bg-border-subtle p-0.5 relative transition-colors"
          >
            <div className={`w-5 h-5 rounded-full bg-primary-blue transition-all ${billingCycle === 'yearly' ? 'translate-x-6' : ''}`} />
          </button>
          <span className={`text-sm ${billingCycle === 'yearly' ? 'text-white font-bold' : 'text-text-muted'} flex items-center gap-1.5`}>
            Yearly
            <span className="text-[10px] font-bold bg-accent-emerald/20 text-accent-emerald px-1.5 py-0.5 rounded-sm">-20%</span>
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto text-left">
          {/* Free */}
          <div className="p-8 rounded-lg bg-card-bg border border-border-strong flex flex-col justify-between hover:border-border-subtle transition-all">
            <div>
              <span className="text-xs font-bold text-text-muted tracking-wider block mb-2 uppercase">FREE FOREVER</span>
              <h3 className="text-3xl font-extrabold text-white mb-6">₹0 <span className="text-sm font-normal text-text-muted">/ month</span></h3>
              <ul className="space-y-4 text-sm text-text-secondary">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Browse all upcoming IPOs</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Basic IPO details</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> 3 AI analyses per month</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Email alerts</li>
              </ul>
            </div>
            <Link href="/register" className="mt-8 w-full border border-border-subtle hover:bg-dark-bg text-white font-semibold py-2.5 rounded-md text-center block transition-colors">
              Get Started Free
            </Link>
          </div>

          {/* Pro */}
          <div className="p-8 rounded-lg bg-card-bg border-2 border-primary-blue relative flex flex-col justify-between shadow-2xl animate-pulse-glow">
            <span className="absolute -top-3.5 left-1/2 -translate-x-1/2 bg-gradient-to-r from-primary-blue to-secondary-purple text-white text-[10px] font-bold px-3 py-1 rounded-full uppercase tracking-wider">
              MOST POPULAR
            </span>
            <div>
              <span className="text-xs font-bold text-primary-blue tracking-wider block mb-2 uppercase">PRO</span>
              <h3 className="text-3xl font-extrabold text-white mb-6">
                {billingCycle === 'monthly' ? '₹499' : '₹399'} <span className="text-sm font-normal text-text-muted">/ month</span>
              </h3>
              <ul className="space-y-4 text-sm text-text-secondary">
                <li className="flex items-center gap-2 text-white font-semibold"><Check className="w-4 h-4 text-accent-emerald" /> Everything in Free</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Unlimited AI analyses</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Full SWOT & Risk reports</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> AI Chat Companion</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Telegram instant notifications</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> GMP live tracker</li>
              </ul>
            </div>
            <Link href="/register" className="mt-8 w-full bg-primary-blue hover:bg-blue-700 text-white font-semibold py-2.5 rounded-md text-center block transition-colors">
              Upgrade to Pro
            </Link>
          </div>

          {/* Enterprise */}
          <div className="p-8 rounded-lg bg-card-bg border border-border-strong flex flex-col justify-between hover:border-border-subtle transition-all">
            <div>
              <span className="text-xs font-bold text-text-muted tracking-wider block mb-2 uppercase">ENTERPRISE</span>
              <h3 className="text-3xl font-extrabold text-white mb-6">Custom</h3>
              <ul className="space-y-4 text-sm text-text-secondary">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> All Pro features</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> API data integration endpoints</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Custom weekly research exports</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-accent-emerald" /> Dedicated analyst support</li>
              </ul>
            </div>
            <Link href="/contact" className="mt-8 w-full border border-border-subtle hover:bg-dark-bg text-white font-semibold py-2.5 rounded-md text-center block transition-colors">
              Contact Sales
            </Link>
          </div>
        </div>
      </section>

      {/* Pricing Billing FAQs */}
      <section className="py-16 px-6 max-w-3xl mx-auto w-full mb-16 border-t border-border-strong/50">
        <h2 className="text-2xl font-bold text-white text-center mb-8">Billing & Payments FAQ</h2>
        <div className="space-y-4">
          {faqs.map((faq, idx) => (
            <div key={idx} className="p-5 bg-card-bg border border-border-strong rounded-lg flex gap-4">
              <HelpCircle className="w-5 h-5 text-primary-blue shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-white mb-2">{faq.q}</h4>
                <p className="text-sm text-text-secondary leading-relaxed">{faq.a}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <Footer />
    </div>
  );
}
