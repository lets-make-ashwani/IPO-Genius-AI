'use client';

import { use, useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  ArrowLeft, 
  Sparkles, 
  AlertTriangle,
  FileText,
  Activity,
  Award,
  CheckCircle,
  RefreshCw
} from 'lucide-react';
import { ipoService } from '../../../../../services/ipo.service';
import { IPO } from '../../../../../types';
import { BackendIPOAnalysis } from '../../../../../types/api';

export default function AIAnalysisPage({ params }: { params: any }) {
  const unwrappedParams = use(params) as any;
  const id = unwrappedParams.id;
  const [ipo, setIpo] = useState<IPO | null>(null);
  const [analysis, setAnalysis] = useState<BackendIPOAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    Promise.all([
      ipoService.getIPOById(id),
      ipoService.getIPOAnalysis(id)
    ]).then(([ipoData, analysisData]) => {
      if (isMounted) {
        if (ipoData) setIpo(ipoData);
        if (analysisData) setAnalysis(analysisData);
        setLoading(false);
      }
    }).catch(err => {
      console.error('Failed to load analysis page:', err);
      if (isMounted) setLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, [id]);

  const handleRegenerate = async () => {
    setAnalyzing(true);
    try {
      const freshAnalysis = await ipoService.getIPOAnalysis(id);
      if (freshAnalysis) setAnalysis(freshAnalysis);
    } catch (err) {
      console.error('Failed to regenerate analysis:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50dvh] text-text-muted">
        <div className="w-8 h-8 rounded-full border-2 border-primary-blue border-t-transparent animate-spin mb-4" />
        Generating Gemini 1.5 Flash AI Rating & Evaluation...
      </div>
    );
  }

  const score = analysis?.overall_score ?? ipo?.aiScore ?? 84;
  const recommendation = analysis?.recommendation ?? ipo?.aiRecommendation ?? 'SUBSCRIBE';
  const summary = analysis?.summary ?? 'Swiggy exhibits strong market leadership in quick commerce with accelerating revenue expansion.';

  return (
    <div className="space-y-6 sm:space-y-8 max-w-full overflow-x-hidden">
      {/* Back button */}
      <Link href={`/dashboard/ipo/${id}`} className="text-xs font-semibold text-text-muted hover:text-white flex items-center gap-1.5 w-fit min-h-[44px]">
        <ArrowLeft className="w-4 h-4" /> Back to IPO Details
      </Link>

      {/* Hero AI Rating Card */}
      <div className="p-4 sm:p-6 bg-gradient-to-br from-card-bg to-dark-bg border border-secondary-purple/30 rounded-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-6 shadow-xl relative overflow-hidden">
        <div className="space-y-2 max-w-xl">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-secondary-purple animate-pulse" />
            <span className="text-xs font-bold text-secondary-purple uppercase tracking-wider">Gemini 1.5 Flash AI Engine</span>
          </div>
          <h1 className="text-xl sm:text-2xl font-extrabold text-white break-words">{ipo?.name || 'IPO'} AI Evaluation</h1>
          <p className="text-xs sm:text-sm text-text-secondary leading-relaxed">{summary}</p>
        </div>

        <div className="flex items-center justify-between md:justify-end gap-6 w-full md:w-auto border-t border-border-subtle/30 md:border-none pt-4 md:pt-0">
          <div className="text-center">
            <div className={`w-16 h-16 sm:w-20 sm:h-20 rounded-full border-4 flex items-center justify-center font-bold text-xl sm:text-2xl font-mono mx-auto ${
              score >= 80 ? 'border-accent-emerald text-accent-emerald' : 'border-yellow-500 text-yellow-500'
            }`}>
              {score}
            </div>
            <span className="text-[10px] text-text-muted font-mono mt-1 block">OVERALL SCORE</span>
          </div>

          <div className="text-left space-y-2">
            <div className="px-3 py-1 rounded-full bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20 text-xs font-bold text-center">
              {recommendation}
            </div>
            <button
              onClick={handleRegenerate}
              disabled={analyzing}
              className="text-xs text-primary-blue hover:underline flex items-center gap-1 disabled:opacity-50 min-h-[44px]"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${analyzing ? 'animate-spin' : ''}`} />
              {analyzing ? 'Evaluating...' : 'Re-Evaluate'}
            </button>
          </div>
        </div>
      </div>

      {/* Metric Breakdown Sub-Scores Grid */}
      <div className="grid grid-cols-1 min-[480px]:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'FINANCIAL HEALTH', score: analysis?.financial_score ?? 86, desc: 'Revenue & Debt ratios' },
          { label: 'MANAGEMENT GRADE', score: analysis?.management_score ?? 83, desc: 'Promoter governance' },
          { label: 'VALUATION MULTIPLE', score: analysis?.valuation_score ?? 80, desc: 'P/E peer comparisons' },
          { label: 'RISK INDEX', score: analysis?.risk_score ?? 25, desc: '25% Low volatility' }
        ].map((item, idx) => (
          <div key={idx} className="p-4 sm:p-5 bg-card-bg border border-border-strong rounded-lg flex justify-between items-center">
            <div>
              <span className="text-[10px] sm:text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">{item.label}</span>
              <span className="text-xl sm:text-2xl font-bold text-white font-mono">{item.score}/100</span>
              <span className="text-[10px] text-text-muted block mt-1">{item.desc}</span>
            </div>
            <Award className="w-6 h-6 text-primary-blue/30 shrink-0" />
          </div>
        ))}
      </div>

      {/* SWOT Matrix Grid */}
      <div className="space-y-4">
        <h2 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
          <Activity className="w-4 h-4 text-primary-blue" /> AI SWOT Matrix
        </h2>

        <div className="grid grid-cols-1 min-[480px]:grid-cols-2 gap-4">
          <div className="p-4 sm:p-6 bg-card-bg border border-border-strong rounded-lg space-y-3">
            <h3 className="font-bold text-accent-emerald text-sm flex items-center gap-1.5">
              <CheckCircle className="w-4 h-4" /> Key Strengths
            </h3>
            <ul className="text-xs text-text-secondary space-y-2 list-disc pl-4">
              <li>Leading market position in Instamart quick commerce logistics</li>
              <li>Hyper-dense urban fulfillment dark store infrastructure</li>
              <li>Strong brand recall across 500+ tier-1 Indian cities</li>
            </ul>
          </div>

          <div className="p-4 sm:p-6 bg-card-bg border border-border-strong rounded-lg space-y-3">
            <h3 className="font-bold text-red-400 text-sm flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4" /> Risk Factors
            </h3>
            <ul className="text-xs text-text-secondary space-y-2 list-disc pl-4">
              <li>Historical operational EBITDA cash burn rate</li>
              <li>Fuel inflation impacting last-mile delivery margins</li>
              <li>Changes in gig worker labor regulation policies</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Official Prospectus Regulatory Links */}
      <div className="p-4 sm:p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
        <h3 className="font-bold text-white text-sm sm:text-base flex items-center gap-2">
          <FileText className="w-4 h-4 text-primary-blue" /> Regulatory Prospectus Documents (SEBI Filings)
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 font-mono text-xs">
          <a
            href={ipo?.drhpUrl || '#'}
            target="_blank"
            rel="noopener noreferrer"
            className="p-3 bg-dark-bg border border-border-subtle hover:border-primary-blue rounded flex items-center justify-between text-primary-blue font-semibold min-h-[44px]"
          >
            <span>Draft Prospectus (DRHP)</span>
            <FileText className="w-4 h-4" />
          </a>
          <a
            href={ipo?.rhpUrl || '#'}
            target="_blank"
            rel="noopener noreferrer"
            className="p-3 bg-dark-bg border border-border-subtle hover:border-primary-blue rounded flex items-center justify-between text-primary-blue font-semibold min-h-[44px]"
          >
            <span>Red Herring (RHP)</span>
            <FileText className="w-4 h-4" />
          </a>
          <a
            href={ipo?.prospectusUrl || '#'}
            target="_blank"
            rel="noopener noreferrer"
            className="p-3 bg-dark-bg border border-border-subtle hover:border-primary-blue rounded flex items-center justify-between text-primary-blue font-semibold min-h-[44px]"
          >
            <span>Final Prospectus PDF</span>
            <FileText className="w-4 h-4" />
          </a>
        </div>
      </div>
    </div>
  );
}
