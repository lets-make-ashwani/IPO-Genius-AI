'use client';

import { use, useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  ArrowLeft, 
  Sparkles, 
  Heart, 
  AlertTriangle, 
  CheckCircle,
  HelpCircle,
  BarChart2,
  Calendar,
  Building,
  DollarSign
} from 'lucide-react';
import { ipoService } from '../../../../services/ipo.service';
import { IPO } from '../../../../types';

export default function IPODetails({ params }: { params: any }) {
  const unwrappedParams = use(params) as any;
  const id = unwrappedParams.id;
  const [ipo, setIpo] = useState<IPO | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'financials' | 'swot'>('overview');
  const [inWatchlist, setInWatchlist] = useState(false);

  useEffect(() => {
    ipoService.getIPOById(id).then((data) => {
      if (data) setIpo(data);
    });
  }, [id]);

  if (!ipo) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-text-muted">
        <div className="w-8 h-8 rounded-full border-2 border-primary-blue border-t-transparent animate-spin mb-4" />
        Loading listing details...
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Back button */}
      <Link href="/dashboard/ipo" className="text-xs font-semibold text-text-muted hover:text-white flex items-center gap-1.5 w-fit">
        <ArrowLeft className="w-4 h-4" /> Back to listings
      </Link>

      {/* Page Header */}
      <div className="bg-card-bg border border-border-strong p-6 rounded-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-lg bg-gradient-to-br from-primary-blue/10 to-secondary-purple/10 flex items-center justify-center font-bold text-primary-blue text-2xl font-mono">
            {ipo.ticker.substring(0, 2)}
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-extrabold text-white">{ipo.name}</h1>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                'bg-primary-blue/10 text-primary-blue border border-primary-blue/20'
              }`}>
                {ipo.status.toUpperCase()}
              </span>
            </div>
            <p className="text-xs text-text-muted mt-1">{ipo.sector} · BSE & NSE Listed</p>
            <div className="flex gap-2 mt-2">
              <span className="text-[10px] bg-dark-bg border border-border-subtle/50 px-2 py-0.5 rounded text-text-secondary font-mono">Ticker: {ipo.ticker}</span>
              <span className="text-[10px] bg-dark-bg border border-border-subtle/50 px-2 py-0.5 rounded text-text-secondary font-mono">Lot Size: {ipo.lotSize} shares</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-6 w-full md:w-auto justify-between md:justify-end border-t border-border-subtle/30 md:border-none pt-4 md:pt-0">
          <div className="flex items-center gap-3">
            <div className={`w-14 h-14 rounded-full border-4 flex items-center justify-center font-bold text-base font-mono ${
              ipo.aiScore >= 80 ? 'border-accent-emerald text-accent-emerald' : 'border-yellow-500 text-yellow-500'
            }`}>
              {ipo.aiScore}
            </div>
            <div className="text-left leading-none">
              <span className="text-[10px] text-text-muted block font-mono">AI SCORE</span>
              <span className="text-xs font-bold text-white">{ipo.aiRecommendation}</span>
            </div>
          </div>

          <div className="flex gap-2">
            <button 
              onClick={() => setInWatchlist(p => !p)}
              className={`p-2.5 rounded-md border transition-colors ${
                inWatchlist ? 'bg-red-500/15 border-red-500/30 text-red-500' : 'border-border-subtle hover:bg-dark-bg text-text-muted hover:text-white'
              }`}
              title="Add to watchlist"
            >
              <Heart className={`w-4 h-4 ${inWatchlist ? 'fill-red-500' : ''}`} />
            </button>
            <Link href={`/dashboard/ipo/${ipo.id}/analysis`} className="bg-secondary-purple hover:bg-purple-700 text-white font-semibold text-xs px-4 py-2.5 rounded-md flex items-center gap-1.5 shadow-lg shadow-secondary-purple/20 transition-all">
              <Sparkles className="w-4 h-4" /> AI Analysis
            </Link>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-border-strong gap-8 text-sm font-semibold">
        {[
          { key: 'overview', label: 'Overview' },
          { key: 'financials', label: 'Financial Statements' },
          { key: 'swot', label: 'SWOT Profile' }
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as any)}
            className={`pb-3 border-b-2 transition-all ${
              activeTab === tab.key ? 'border-primary-blue text-primary-blue' : 'border-transparent text-text-muted hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left main detail */}
        <div className="lg:col-span-8 space-y-8">
          {activeTab === 'overview' && (
            <>
              {/* Overview */}
              <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
                <h3 className="text-white font-bold text-base flex items-center gap-2">
                  <Building className="w-4 h-4 text-primary-blue" /> Company Overview
                </h3>
                <p className="text-sm text-text-secondary leading-relaxed">{ipo.overview}</p>
                <h4 className="font-bold text-white text-sm pt-2">Business Model</h4>
                <p className="text-sm text-text-secondary leading-relaxed">{ipo.businessModel}</p>
              </div>

              {/* Timeline */}
              <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-6">
                <h3 className="text-white font-bold text-base flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-primary-blue" /> IPO Timeline
                </h3>
                <div className="relative flex flex-col md:flex-row justify-between items-start md:items-center w-full gap-6 md:gap-2 before:absolute before:left-3 md:before:left-2 before:right-2 before:top-3 md:before:top-2 before:w-[2px] md:before:w-full before:h-full md:before:h-[2px] before:bg-border-strong before:z-0">
                  {[
                    { label: 'Bids Open', date: ipo.openDate, done: true },
                    { label: 'Bids Close', date: ipo.closeDate, done: true },
                    { label: 'Allotment', date: ipo.allotmentDate, active: true },
                    { label: 'Refunds', date: ipo.refundDate },
                    { label: 'Listing', date: ipo.listingDate }
                  ].map((node, idx) => (
                    <div key={idx} className="relative z-10 flex md:flex-col items-center gap-3 md:gap-2 text-left md:text-center pl-6 md:pl-0">
                      <div className={`w-5 h-5 rounded-full border-4 bg-dark-bg flex items-center justify-center ${
                        node.done ? 'border-accent-emerald text-accent-emerald' :
                        node.active ? 'border-primary-blue text-primary-blue animate-pulse' :
                        'border-border-strong'
                      }`} />
                      <div className="leading-none">
                        <span className="text-[10px] font-bold text-white block mb-0.5">{node.label}</span>
                        <span className="text-[10px] text-text-muted font-mono">{new Date(node.date).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Strengths / Risks */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
                  <h3 className="text-accent-emerald font-bold text-base flex items-center gap-2">
                    <CheckCircle className="w-4 h-4" /> Operational Strengths
                  </h3>
                  <ul className="space-y-3">
                    {ipo.strengths.map((str, idx) => (
                      <li key={idx} className="text-xs text-text-secondary leading-relaxed flex gap-2">
                        <span className="text-accent-emerald font-bold shrink-0">•</span>
                        <span>{str}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
                  <h3 className="text-red-400 font-bold text-base flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4" /> Risk Factors
                  </h3>
                  <ul className="space-y-3">
                    {ipo.risks.map((risk, idx) => (
                      <li key={idx} className="text-xs text-text-secondary leading-relaxed flex gap-2">
                        <span className="text-red-400 font-bold shrink-0">•</span>
                        <span>{risk}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </>
          )}

          {activeTab === 'financials' && (
            <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-6">
              <h3 className="text-white font-bold text-base flex items-center gap-2">
                <BarChart2 className="w-4 h-4 text-primary-blue" /> Financial Summary
              </h3>
              <p className="text-xs text-text-muted leading-relaxed">Figures listed below are in Crores (INR) sourced directly from audit documentation files.</p>
              
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-xs">
                  <thead>
                    <tr className="border-b border-border-strong bg-dark-bg/40 font-bold text-text-muted uppercase tracking-wider">
                      <th className="p-3 pl-4">Metrics (₹ Cr)</th>
                      {ipo.financialSummary.years.map(y => <th key={y} className="p-3 font-mono">{y}</th>)}
                    </tr>
                  </thead>
                  <tbody className="text-text-secondary divide-y divide-border-strong/30">
                    <tr className="hover:bg-dark-bg/25">
                      <td className="p-3 pl-4 font-semibold text-white">Revenue</td>
                      {ipo.financialSummary.revenue.map((val, i) => <td key={i} className="p-3 font-mono">₹{val} Cr</td>)}
                    </tr>
                    <tr className="hover:bg-dark-bg/25">
                      <td className="p-3 pl-4 font-semibold text-white">EBITDA</td>
                      {ipo.financialSummary.ebitda.map((val, i) => <td key={i} className="p-3 font-mono">₹{val} Cr</td>)}
                    </tr>
                    <tr className="hover:bg-dark-bg/25">
                      <td className="p-3 pl-4 font-semibold text-white">Net Profit</td>
                      {ipo.financialSummary.profit.map((val, i) => <td key={i} className="p-3 font-mono {val < 0 ? 'text-red-400' : 'text-accent-emerald'}">
                        {val < 0 ? `-₹${Math.abs(val)}` : `₹${val}`} Cr
                      </td>)}
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'swot' && (
            <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-6">
              <h3 className="text-white font-bold text-base flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-secondary-purple" /> SWOT Analysis
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-4 rounded-md bg-emerald-500/5 border border-accent-emerald/20 space-y-2">
                  <h4 className="font-bold text-accent-emerald text-sm uppercase">S - Strengths</h4>
                  <ul className="space-y-1.5 text-xs text-text-secondary">
                    {ipo.swot.strengths.map((s, i) => <li key={i}>• {s}</li>)}
                  </ul>
                </div>
                <div className="p-4 rounded-md bg-red-500/5 border border-red-500/20 space-y-2">
                  <h4 className="font-bold text-red-400 text-sm uppercase">W - Weaknesses</h4>
                  <ul className="space-y-1.5 text-xs text-text-secondary">
                    {ipo.swot.weaknesses.map((w, i) => <li key={i}>• {w}</li>)}
                  </ul>
                </div>
                <div className="p-4 rounded-md bg-blue-500/5 border border-primary-blue/20 space-y-2">
                  <h4 className="font-bold text-primary-blue text-sm uppercase">O - Opportunities</h4>
                  <ul className="space-y-1.5 text-xs text-text-secondary">
                    {ipo.swot.opportunities.map((o, i) => <li key={i}>• {o}</li>)}
                  </ul>
                </div>
                <div className="p-4 rounded-md bg-yellow-500/5 border border-yellow-500/20 space-y-2">
                  <h4 className="font-bold text-yellow-500 text-sm uppercase">T - Threats</h4>
                  <ul className="space-y-1.5 text-xs text-text-secondary">
                    {ipo.swot.threats.map((t, i) => <li key={i}>• {t}</li>)}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Info Panel Sidebar */}
        <div className="lg:col-span-4 space-y-6">
          <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-6">
            <h3 className="font-bold text-white text-base flex items-center gap-2">
              <DollarSign className="w-4 h-4 text-primary-blue" /> Issue Details
            </h3>
            
            <div className="space-y-4 text-xs">
              {[
                { label: 'Price Band', val: `₹${ipo.priceBand.min} - ₹${ipo.priceBand.max}`, highlight: true },
                { label: 'GMP Premium', val: `+${ipo.gmp}%`, success: true },
                { label: 'Issue Size', val: `₹${ipo.issueSize} Cr` },
                { label: 'Lot Size', val: `${ipo.lotSize} Shares` },
                { label: 'Min Investment', val: `₹${ipo.priceBand.min * ipo.lotSize}` }
              ].map((row, idx) => (
                <div key={idx} className="flex justify-between items-center py-2 border-b border-border-subtle/25 last:border-none">
                  <span className="text-text-muted">{row.label}</span>
                  <span className={`font-bold font-mono ${
                    row.highlight ? 'text-white text-sm' :
                    row.success ? 'text-accent-emerald text-sm' : 'text-text-secondary'
                  }`}>{row.val}</span>
                </div>
              ))}
            </div>

            <button className="w-full h-11 bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs rounded-md shadow-md transition-colors">
              Apply via UPI broker
            </button>
          </div>
          
          <div className="p-6 bg-card-bg border-2 border-primary-blue/30 rounded-lg space-y-4 relative overflow-hidden animate-pulse-glow">
            <h3 className="font-bold text-white text-sm flex items-center gap-1.5 text-secondary-purple">
              <Sparkles className="w-4 h-4" /> AI Evaluation Index
            </h3>
            <p className="text-xs text-text-secondary leading-relaxed">
              Consolidated strength ratings compared against historical listing metrics. Rating shifts based on actual subscription scales during bidding.
            </p>
            <div className="pt-2">
              <Link href={`/dashboard/ipo/${ipo.id}/analysis`} className="text-xs font-semibold text-primary-blue hover:underline flex items-center gap-1.5">
                Open AI Report page →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
