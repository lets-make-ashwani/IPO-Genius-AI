'use client';

import { use, useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  ArrowLeft, 
  Sparkles, 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle,
  FileText,
  Activity,
  Award
} from 'lucide-react';
import { ipoService } from '../../../../../services/ipo.service';
import { IPO } from '../../../../../types';

export default function AIAnalysis({ params }: { params: any }) {
  const unwrappedParams = use(params) as any;
  const id = unwrappedParams.id;
  const [ipo, setIpo] = useState<IPO | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    ipoService.getIPOById(id).then((data) => {
      if (data) setIpo(data);
    });
  }, [id]);

  const handleRegenerate = async () => {
    setAnalyzing(true);
    try {
      const updated = await ipoService.triggerAIAnalysis(id);
      setIpo(updated);
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  if (!ipo) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-text-muted">
        <div className="w-8 h-8 rounded-full border-2 border-primary-blue border-t-transparent animate-spin mb-4" />
        Loading AI engine data...
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Back button */}
      <Link href={`/dashboard/ipo/${ipo.id}`} className="text-xs font-semibold text-text-muted hover:text-white flex items-center gap-1.5 w-fit">
        <ArrowLeft className="w-4 h-4" /> Back to {ipo.name}
      </Link>

      {/* Page Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-strong pb-5">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-md bg-secondary-purple/10 text-secondary-purple">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl font-extrabold text-white flex items-center gap-2">AI Analysis Report</h1>
            <p className="text-xs text-text-muted">Deep evaluation models for {ipo.name} ({ipo.ticker})</p>
          </div>
        </div>
        
        <button
          onClick={handleRegenerate}
          disabled={analyzing}
          className="bg-secondary-purple hover:bg-purple-700 disabled:opacity-50 text-white font-semibold text-xs px-4 py-2.5 rounded-md flex items-center gap-1.5 transition-all"
        >
          <Sparkles className="w-4 h-4" />
          {analyzing ? 'Evaluating...' : 'Regenerate Analysis'}
        </button>
      </div>

      {analyzing ? (
        <div className="flex flex-col items-center justify-center h-96 text-center space-y-4">
          <div className="p-4 rounded-full bg-secondary-purple/10 text-secondary-purple animate-pulse-glow">
            <Sparkles className="w-10 h-10 animate-spin" />
          </div>
          <h3 className="text-white font-bold text-lg">Running AI Analysis Engine</h3>
          <p className="text-sm text-text-secondary max-w-sm">Scanning 47 prospectus parameters, evaluation grids, and financial liabilities...</p>
        </div>
      ) : (
        <>
          {/* Top Analytics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* AI Score */}
            <div className="p-6 bg-card-bg border-2 border-primary-blue/20 rounded-lg flex flex-col items-center justify-center text-center relative overflow-hidden animate-pulse-glow">
              <div className="absolute top-0 right-0 -translate-y-8 translate-x-8 w-24 h-24 bg-primary-blue/5 rounded-full blur-[40px]" />
              
              <div className="relative mb-4 flex items-center justify-center">
                <div className={`w-32 h-32 rounded-full border-8 flex flex-col items-center justify-center font-extrabold font-mono ${
                  ipo.aiScore >= 80 ? 'border-accent-emerald text-accent-emerald' : 'border-yellow-500 text-yellow-500'
                }`}>
                  <span className="text-3xl">{ipo.aiScore}</span>
                  <span className="text-[10px] text-text-muted mt-0.5">/100</span>
                </div>
              </div>
              <h3 className="font-bold text-white text-sm mb-1">AI Recommendation Score</h3>
              <p className="text-[10px] text-text-muted">Calculated relative to 500+ historical deal outcomes.</p>
            </div>

            {/* Recommendation */}
            <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between">
              <div className="space-y-4">
                <span className="text-[10px] font-bold text-text-muted block uppercase tracking-wider">AI Verdict</span>
                <span className="text-3xl font-extrabold text-accent-emerald block font-mono">{ipo.aiRecommendation.toUpperCase()}</span>
                <p className="text-xs text-text-secondary leading-relaxed">
                  Based on prospectus indicators, this deal represents a high probability listing gain outcome. The growth trajectory justifies investment.
                </p>
              </div>
              <div className="space-y-1.5 text-xs pt-4 border-t border-border-subtle/30">
                <div className="flex justify-between font-semibold">
                  <span className="text-text-muted">Confidence Level</span>
                  <span className="text-accent-emerald">87%</span>
                </div>
                <div className="w-full h-1.5 bg-dark-bg rounded-full overflow-hidden">
                  <div className="h-full bg-accent-emerald rounded-full" style={{ width: '87%' }} />
                </div>
              </div>
            </div>

            {/* Stats Overview */}
            <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between">
              <div className="space-y-4">
                <span className="text-[10px] font-bold text-text-muted block uppercase tracking-wider">Key Indicators</span>
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div>
                    <span className="text-text-muted block mb-0.5">PE Ratio</span>
                    <span className="font-bold text-white font-mono">34.6x</span>
                  </div>
                  <div>
                    <span className="text-text-muted block mb-0.5">GMP Premium</span>
                    <span className="font-bold text-accent-emerald font-mono">+{ipo.gmp}%</span>
                  </div>
                  <div>
                    <span className="text-text-muted block mb-0.5">Revenue Growth</span>
                    <span className="font-bold text-white font-mono">+43% YoY</span>
                  </div>
                  <div>
                    <span className="text-text-muted block mb-0.5">Net Debt</span>
                    <span className="font-bold text-white font-mono">₹450 Cr</span>
                  </div>
                </div>
              </div>
              <div className="pt-4 border-t border-border-subtle/30 text-[10px] text-text-muted flex items-center gap-1.5">
                <Award className="w-4 h-4 text-primary-blue" /> Evaluated on 47 Prospectus parameters.
              </div>
            </div>
          </div>

          {/* SWOT Grid */}
          <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-6">
            <h3 className="font-bold text-white text-base flex items-center gap-2">
              <FileText className="w-4 h-4 text-primary-blue" /> Detailed SWOT Profile
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="p-5 rounded bg-emerald-500/5 border border-accent-emerald/20 space-y-3">
                <h4 className="font-bold text-accent-emerald text-sm uppercase flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-accent-emerald" /> Strengths
                </h4>
                <ul className="space-y-2 text-xs text-text-secondary leading-relaxed">
                  {ipo.swot.strengths.map((s, i) => <li key={i} className="flex gap-2"><span>•</span> <span>{s}</span></li>)}
                </ul>
              </div>
              <div className="p-5 rounded bg-red-500/5 border border-red-500/20 space-y-3">
                <h4 className="font-bold text-red-400 text-sm uppercase flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-red-400" /> Weaknesses
                </h4>
                <ul className="space-y-2 text-xs text-text-secondary leading-relaxed">
                  {ipo.swot.weaknesses.map((w, i) => <li key={i} className="flex gap-2"><span>•</span> <span>{w}</span></li>)}
                </ul>
              </div>
              <div className="p-5 rounded bg-blue-500/5 border border-primary-blue/20 space-y-3">
                <h4 className="font-bold text-primary-blue text-sm uppercase flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-primary-blue" /> Opportunities
                </h4>
                <ul className="space-y-2 text-xs text-text-secondary leading-relaxed">
                  {ipo.swot.opportunities.map((o, i) => <li key={i} className="flex gap-2"><span>•</span> <span>{o}</span></li>)}
                </ul>
              </div>
              <div className="p-5 rounded bg-yellow-500/5 border border-yellow-500/20 space-y-3">
                <h4 className="font-bold text-yellow-500 text-sm uppercase flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-yellow-500" /> Threats
                </h4>
                <ul className="space-y-2 text-xs text-text-secondary leading-relaxed">
                  {ipo.swot.threats.map((t, i) => <li key={i} className="flex gap-2"><span>•</span> <span>{t}</span></li>)}
                </ul>
              </div>
            </div>
          </div>

          {/* Risk Factors progress bars */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-6">
              <h3 className="font-bold text-white text-base flex items-center gap-2">
                <Activity className="w-4 h-4 text-primary-blue" /> Risk Level Breakdown
              </h3>
              <div className="space-y-4">
                {[
                  { label: 'Market Risk', level: 'Low', val: 30, color: 'bg-accent-emerald' },
                  { label: 'Financial Debt Risk', level: 'Medium', val: 55, color: 'bg-yellow-500' },
                  { label: 'Regulatory Risk', level: 'High', val: 80, color: 'bg-red-500' },
                  { label: 'Valuation Premium', level: 'Medium', val: 65, color: 'bg-yellow-500' }
                ].map((risk, idx) => (
                  <div key={idx} className="space-y-1.5 text-xs">
                    <div className="flex justify-between font-semibold">
                      <span className="text-text-secondary">{risk.label}</span>
                      <span className="text-text-muted">{risk.level}</span>
                    </div>
                    <div className="w-full h-2 bg-dark-bg rounded-full overflow-hidden">
                      <div className={`h-full ${risk.color} rounded-full`} style={{ width: `${risk.val}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* AI Summary Conclusion */}
            <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between">
              <div className="space-y-4">
                <h3 className="font-bold text-white text-base flex items-center gap-1.5 text-secondary-purple">
                  <Sparkles className="w-4 h-4" /> AI Report Conclusion
                </h3>
                <p className="text-xs text-text-secondary leading-relaxed">
                  Swiggy Ltd demonstrates favorable unit economics and Instamart quick commerce market consolidation. Although cash burn remains a structural weakness, the relative valuation PE multiple of 34.6x (compared to Zomato's 60x+) makes this a prime listing candidate. Recommendation: Apply for short-term Listing gains with low-moderate risk profiles.
                </p>
              </div>
              
              <div className="p-4 bg-yellow-500/5 border border-yellow-500/20 text-[10px] text-yellow-500 italic rounded-md mt-6 leading-relaxed">
                ⚠ AI evaluations are generated using automated prospectuses crawlers and sentiment charts. This does not represent official financial advising models. Allocate capital at your own discretion.
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
