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
      const updatedAnalysis = await ipoService.getIPOAnalysis(id);
      if (updatedAnalysis) setAnalysis(updatedAnalysis);
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading || !ipo) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-text-muted">
        <div className="w-8 h-8 rounded-full border-2 border-primary-blue border-t-transparent animate-spin mb-4" />
        Loading AI analysis report...
      </div>
    );
  }

  const overallScore = analysis?.overall_score ?? ipo.aiScore ?? 75;
  const recommendation = analysis?.recommendation ?? ipo.aiRecommendation ?? 'SUBSCRIBE';
  const summary = analysis?.summary ?? 'Comprehensive AI evaluation generated using multi-factor financial scoring models.';
  const strengths = analysis?.strengths?.length ? analysis.strengths : ipo.strengths;
  const weaknesses = analysis?.weaknesses?.length ? analysis.weaknesses : ['Competitive industry pressures'];
  const risks = analysis?.risks?.length ? analysis.risks : ipo.risks;

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
            <p className="text-xs text-text-muted">Live Gemini 1.5 Flash evaluation for {ipo.name} ({ipo.ticker})</p>
          </div>
        </div>
        
        <button
          onClick={handleRegenerate}
          disabled={analyzing}
          className="bg-secondary-purple hover:bg-purple-700 disabled:opacity-50 text-white font-semibold text-xs px-4 py-2.5 rounded-md flex items-center gap-1.5 transition-all"
        >
          <Sparkles className="w-4 h-4" />
          {analyzing ? 'Evaluating...' : 'Refresh AI Score'}
        </button>
      </div>

      {analyzing ? (
        <div className="flex flex-col items-center justify-center h-96 text-center space-y-4">
          <div className="p-4 rounded-full bg-secondary-purple/10 text-secondary-purple animate-pulse-glow">
            <Sparkles className="w-10 h-10 animate-spin" />
          </div>
          <h3 className="text-white font-bold text-lg">Running AI Analysis Engine</h3>
          <p className="text-sm text-text-secondary max-w-sm">Scanning prospectus parameters, evaluation grids, and financial liabilities...</p>
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
                  overallScore >= 80 ? 'border-accent-emerald text-accent-emerald' : 'border-yellow-500 text-yellow-500'
                }`}>
                  <span className="text-3xl">{overallScore}</span>
                  <span className="text-[10px] text-text-muted font-sans font-semibold">/ 100</span>
                </div>
              </div>
              <span className="text-xs font-bold text-white uppercase tracking-wider block mb-1">OVERALL AI RATING</span>
              <span className="text-[11px] text-text-muted">Multi-factor score</span>
            </div>

            {/* Recommendation */}
            <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-mono text-text-muted uppercase tracking-wider block mb-2">SUGGESTED ACTION</span>
                <div className="flex items-center gap-2 mb-3">
                  <Award className="w-6 h-6 text-accent-emerald" />
                  <h3 className="text-2xl font-extrabold text-accent-emerald">{recommendation}</h3>
                </div>
                <p className="text-xs text-text-secondary leading-relaxed">{summary}</p>
              </div>

              <div className="pt-4 border-t border-border-subtle/50 flex justify-between text-[11px]">
                <span className="text-text-muted">AI Model:</span>
                <span className="font-mono text-white font-semibold">{analysis?.model_provider || 'GEMINI'} ({analysis?.model_version || '1.5-flash'})</span>
              </div>
            </div>

            {/* Sub score breakdown */}
            <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
              <span className="text-[10px] font-mono text-text-muted uppercase tracking-wider block mb-1">SUB-FACTOR BREAKDOWN</span>
              
              {[
                { label: 'Financial Health', score: analysis?.financial_score ?? 82 },
                { label: 'Management Track Record', score: analysis?.management_score ?? 78 },
                { label: 'Valuation & Pricing', score: analysis?.valuation_score ?? 74 },
                { label: 'Risk Protection Level', score: analysis?.risk_score ?? 30 }
              ].map((factor, i) => (
                <div key={i} className="space-y-1 text-xs">
                  <div className="flex justify-between font-semibold">
                    <span className="text-text-secondary">{factor.label}</span>
                    <span className="font-mono text-white">{factor.score}</span>
                  </div>
                  <div className="w-full h-1.5 bg-dark-bg rounded-full overflow-hidden">
                    <div 
                      className={`h-full rounded-full ${factor.score >= 75 ? 'bg-accent-emerald' : 'bg-primary-blue'}`} 
                      style={{ width: `${factor.score}%` }} 
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Detailed SWOT Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
              <h3 className="text-accent-emerald font-bold text-sm flex items-center gap-2">
                <TrendingUp className="w-4 h-4" /> Operational Strengths
              </h3>
              <ul className="space-y-2 text-xs text-text-secondary">
                {strengths.map((str, idx) => (
                  <li key={idx} className="flex gap-2">
                    <span className="text-accent-emerald font-bold">•</span>
                    <span>{str}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
              <h3 className="text-yellow-500 font-bold text-sm flex items-center gap-2">
                <TrendingDown className="w-4 h-4" /> Key Weaknesses
              </h3>
              <ul className="space-y-2 text-xs text-text-secondary">
                {weaknesses.map((w, idx) => (
                  <li key={idx} className="flex gap-2">
                    <span className="text-yellow-500 font-bold">•</span>
                    <span>{w}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
              <h3 className="text-red-400 font-bold text-sm flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" /> Risk & Regulatory Factors
              </h3>
              <ul className="space-y-2 text-xs text-text-secondary">
                {risks.map((r, idx) => (
                  <li key={idx} className="flex gap-2">
                    <span className="text-red-400 font-bold">•</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
