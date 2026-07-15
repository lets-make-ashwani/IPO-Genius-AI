'use client';

import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import Link from 'next/link';
import {
  Sparkles,
  Calendar,
  MessageSquare,
  Bell,
  Star,
  Layers,
  ArrowRight,
  TrendingUp,
  ShieldAlert,
  PieChart
} from 'lucide-react';

export default function Features() {
  const featuresList = [
    {
      icon: Sparkles,
      color: 'text-secondary-purple bg-secondary-purple/10',
      title: 'AI-Powered Score Engine',
      desc: 'Our neural network parses the complete Draft Red Herring Prospectus (DRHP) to generate a consolidated IPO rating (0-100) and recommendation index.',
      details: ['Scans 40+ corporate evaluation nodes', 'Compares relative peer valuation multipliers', 'Historical promoter success record scoring']
    },
    {
      icon: Calendar,
      color: 'text-primary-blue bg-primary-blue/10',
      title: 'Dynamic IPO Calendar',
      desc: 'An automated live timeline tracking draft filings, approval states, opening bids, allotment releases, and exchange listings.',
      details: ['Real-time date status changes', 'Automatic Google Calendar synching', 'Time zone adjusted notifications']
    },
    {
      icon: MessageSquare,
      color: 'text-secondary-purple bg-secondary-purple/10',
      title: 'Contextual AI Assistant Chat',
      desc: 'Ask complex finance queries. Get instant responses detailing balance sheet liabilities, debt-to-equity ratios, or potential tax litigations.',
      details: ['Natural language financial processing', 'IPO document-specific indexing', 'Multi-turn conversational tracking']
    },
    {
      icon: Bell,
      color: 'text-primary-blue bg-primary-blue/10',
      title: 'n8n Alert Automation',
      desc: 'Connect our platform directly to your email or Telegram inbox. Receive live alert triggers for GMP changes and bidding reminders.',
      details: ['Custom alert condition toggling', 'Low latency Telegram broadcasts', 'Daily summaries report delivery']
    },
    {
      icon: Star,
      color: 'text-accent-emerald bg-accent-emerald/10',
      title: 'Custom Watchlist Hub',
      desc: 'Create personalized tracking folders for preferred listings. Sort by score, sector, issue size, or opening dates.',
      details: ['GMP price deviation analytics', 'Quick allotment state checks', 'Email watch-summaries']
    },
    {
      icon: Layers,
      color: 'text-primary-blue bg-primary-blue/10',
      title: 'SWOT Quadrant Analytics',
      desc: 'Instant visualization of corporate strengths, operational weaknesses, expansion opportunities, and external market threats.',
      details: ['Color-coded 4-quadrant layout', 'Concise actionable summary bullet points', 'Regulatory litigation risks assessment']
    }
  ];

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col pt-16">
      <Navbar />

      {/* Hero */}
      <section className="py-20 px-6 text-center max-w-4xl mx-auto">
        <span className="text-xs font-bold bg-primary-blue/15 text-primary-blue px-3.5 py-1.5 rounded-full uppercase tracking-wider mb-4 inline-block">
          All Features
        </span>
        <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-6">
          Powerful Features Built for IPO Investors
        </h1>
        <p className="text-lg text-text-secondary">
          Everything you need to discover, analyze, and track upcoming IPOs — powered by financial intelligence.
        </p>
      </section>

      {/* Detailed Features Grid */}
      <section className="py-12 px-6 max-w-6xl mx-auto w-full space-y-16 mb-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <div className="p-3 rounded-md bg-secondary-purple/10 text-secondary-purple w-fit">
              <Sparkles className="w-6 h-6" />
            </div>
            <h2 className="text-2xl md:text-3xl font-bold text-white">AI-Powered Prospectus Analytics</h2>
            <p className="text-text-secondary leading-relaxed">
              Skip reading 400-page prospectus documents. Our AI parses historical balance sheets, cash flows, litigation notes, and promoter histories to summarize strengths and critical risk factors in seconds.
            </p>
            <ul className="space-y-2.5 text-sm text-text-secondary">
              <li className="flex items-center gap-2">✓ Instantly extract debt ratios and profit margins</li>
              <li className="flex items-center gap-2">✓ Uncover hidden promoter pledged share liabilities</li>
              <li className="flex items-center gap-2">✓ Benchmark relative sector valuation multipliers</li>
            </ul>
          </div>
          <div className="p-8 rounded-lg bg-card-bg border border-border-strong flex flex-col gap-6 shadow-xl">
            <h4 className="font-bold text-white text-sm tracking-wider text-text-muted uppercase">ANALYSIS DASHBOARD</h4>
            <div className="space-y-4">
              <div className="flex justify-between items-center bg-dark-bg p-4 rounded-md border border-border-subtle">
                <span className="text-sm font-semibold">Overall AI Rating</span>
                <span className="text-lg font-bold text-accent-emerald">87/100</span>
              </div>
              <div className="flex justify-between items-center bg-dark-bg p-4 rounded-md border border-border-subtle">
                <span className="text-sm font-semibold">Recommendation</span>
                <span className="text-sm font-bold bg-accent-emerald/20 text-accent-emerald px-2 py-0.5 rounded-sm">STRONG BUY</span>
              </div>
              <div className="bg-dark-bg p-4 rounded-md border border-border-subtle text-xs space-y-2">
                <h5 className="font-bold text-secondary-purple">AI Core Verdict</h5>
                <p className="text-text-secondary leading-relaxed">Swiggy Ltd shows exceptional customer cohort retention andInstamart scaling. Buy for listing day gains + long term.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-12 border-t border-border-strong/50">
          {featuresList.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div key={idx} className="p-8 rounded-lg bg-card-bg border border-border-strong flex flex-col justify-between hover:border-primary-blue/30 transition-all">
                <div className="space-y-4">
                  <div className={`p-3 rounded-md w-fit ${feat.color}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="text-lg font-bold text-white">{feat.title}</h3>
                  <p className="text-sm text-text-secondary leading-relaxed">{feat.desc}</p>
                </div>
                <div className="mt-6 pt-4 border-t border-border-subtle/30 space-y-2">
                  {feat.details.map((detail, dIdx) => (
                    <span key={dIdx} className="text-xs text-text-muted block">• {detail}</span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* CTA */}
      <section className="bg-sidebar-bg/60 border-t border-border-subtle py-20 px-6 text-center">
        <div className="max-w-xl mx-auto flex flex-col gap-4">
          <h2 className="text-2xl md:text-3xl font-bold text-white">Invest Smarter Today</h2>
          <p className="text-sm text-text-secondary">Join thousands of retail traders making informed allocations with AI.</p>
          <div className="flex justify-center gap-4 mt-4">
            <Link href="/register" className="bg-primary-blue hover:bg-blue-700 text-white font-semibold px-6 py-2.5 rounded-md text-sm transition-colors flex items-center gap-2">
              Start Free Trial <ArrowRight className="w-4 h-4" />
            </Link>
            <Link href="/pricing" className="border border-border-subtle hover:bg-card-bg text-white font-semibold px-6 py-2.5 rounded-md text-sm transition-colors">
              View Pricing Plans
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
