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
  DollarSign,
  FileText
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
      <div className="flex flex-col items-center justify-center min-h-[50dvh] text-text-muted">
        <div className="w-8 h-8 rounded-full border-2 border-primary-blue border-t-transparent animate-spin mb-4" />
        Loading listing details...
      </div>
    );
  }

  return (
    <div className="space-y-6 sm:space-y-8 max-w-full overflow-x-hidden">
      {/* Back button */}
      <Link href="/dashboard/ipo" className="text-xs font-semibold text-text-muted hover:text-white flex items-center gap-1.5 w-fit min-h-[44px]">
        <ArrowLeft className="w-4 h-4" /> Back to listings
      </Link>

      {/* Page Header Card */}
      <div className="bg-card-bg border border-border-strong p-4 sm:p-6 rounded-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4 sm:gap-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 w-full md:w-auto">
          <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-lg bg-gradient-to-br from-primary-blue/10 to-secondary-purple/10 flex items-center justify-center font-bold text-primary-blue text-xl sm:text-2xl font-mono shrink-0">
            {ipo.ticker.substring(0, 2)}
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2 sm:gap-3 mb-1">
              <h1 className="text-xl sm:text-2xl font-extrabold text-white break-words">{ipo.name}</h1>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full shrink-0 ${
                ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                'bg-primary-blue/10 text-primary-blue border border-primary-blue/20'
              }`}>
                {ipo.status.toUpperCase()}
              </span>
            </div>
            <p className="text-xs text-text-muted">{ipo.sector} · BSE & NSE Listed</p>
            <div className="flex flex-wrap gap-2 mt-2">
              <span className="text-[10px] bg-dark-bg border border-border-subtle/50 px-2 py-0.5 rounded text-text-secondary font-mono">Ticker: {ipo.ticker}</span>
              <span className="text-[10px] bg-dark-bg border border-border-subtle/50 px-2 py-0.5 rounded text-text-secondary font-mono">Lot Size: {ipo.lotSize} shares</span>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap sm:flex-nowrap items-center gap-4 w-full md:w-auto justify-between md:justify-end border-t border-border-subtle/30 md:border-none pt-4 md:pt-0">
          <div className="flex items-center gap-3">
            <div className={`w-12 h-12 sm:w-14 sm:h-14 rounded-full border-4 flex items-center justify-center font-bold text-sm sm:text-base font-mono ${
              ipo.aiScore >= 80 ? 'border-accent-emerald text-accent-emerald' : 'border-yellow-500 text-yellow-500'
            }`}>
              {ipo.aiScore}
            </div>
            <div className="text-left leading-none">
              <span className="text-[10px] text-text-muted block font-mono">AI RATING</span>
              <span className="text-xs font-bold text-white">{ipo.aiRecommendation}</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button 
              onClick={() => setInWatchlist(p => !p)}
              className={`p-2.5 rounded-md border transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center ${
                inWatchlist ? 'bg-red-500/15 border-red-500/30 text-red-500' : 'border-border-subtle hover:bg-dark-bg text-text-muted hover:text-white'
              }`}
              title="Add to watchlist"
              aria-label="Add to watchlist"
            >
              <Heart className={`w-4 h-4 ${inWatchlist ? 'fill-red-500' : ''}`} />
            </button>
            <Link href={`/dashboard/ipo/${ipo.id}/analysis`} className="bg-secondary-purple hover:bg-purple-700 text-white font-semibold text-xs px-4 py-2.5 rounded-md flex items-center gap-1.5 shadow-lg shadow-secondary-purple/20 transition-all min-h-[44px]">
              <Sparkles className="w-4 h-4" /> AI Review
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Cards (Price Band, GMP, Issue Size, Listing Date) */}
      <div className="grid grid-cols-1 min-[480px]:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 sm:p-5 bg-card-bg border border-border-strong rounded-lg">
          <span className="text-[10px] sm:text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">PRICE BAND</span>
          <span className="text-xl sm:text-2xl font-bold text-white font-mono block">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</span>
        </div>

        <div className="p-4 sm:p-5 bg-card-bg border border-border-strong rounded-lg">
          <span className="text-[10px] sm:text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">GMP PREMIUM</span>
          <span className="text-xl sm:text-2xl font-bold text-accent-emerald font-mono block">+{ipo.gmp}%</span>
        </div>

        <div className="p-4 sm:p-5 bg-card-bg border border-border-strong rounded-lg">
          <span className="text-[10px] sm:text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">ISSUE SIZE</span>
          <span className="text-xl sm:text-2xl font-bold text-white font-mono block">₹{ipo.issueSize} Cr</span>
        </div>

        <div className="p-4 sm:p-5 bg-card-bg border border-border-strong rounded-lg">
          <span className="text-[10px] sm:text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">LISTING DATE</span>
          <span className="text-xl sm:text-2xl font-bold text-white font-mono block">{ipo.listingDate || 'TBA'}</span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-border-strong gap-2 overflow-x-auto pb-1">
        {[
          { key: 'overview', label: 'Company Overview' },
          { key: 'financials', label: 'Financial Summary' },
          { key: 'swot', label: 'SWOT Analysis' },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as any)}
            className={`px-4 py-2.5 text-xs font-bold transition-all border-b-2 whitespace-nowrap min-h-[44px] ${
              activeTab === tab.key
                ? 'border-primary-blue text-primary-blue bg-primary-blue/5'
                : 'border-transparent text-text-muted hover:text-white'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Panels */}
      {activeTab === 'overview' && (
        <div className="p-4 sm:p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
          <h3 className="font-bold text-white text-base">About {ipo.name}</h3>
          <p className="text-xs sm:text-sm text-text-secondary leading-relaxed">
            {ipo.about}
          </p>
          <div className="pt-4 border-t border-border-subtle flex flex-wrap gap-4 text-xs font-mono text-text-muted">
            <span>REGISTRAR: Link Intime India Pvt Ltd</span>
            <span>LEAD MANAGER: Kotak Mahindra Capital</span>
          </div>
        </div>
      )}

      {activeTab === 'financials' && (
        <div className="p-4 sm:p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
          <h3 className="font-bold text-white text-base">Financial Key Metrics</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono text-xs">
            <div className="p-4 bg-dark-bg rounded border border-border-subtle">
              <span className="text-text-muted block text-[10px]">FY24 REVENUE</span>
              <span className="text-lg font-bold text-white">₹11,247 Cr</span>
            </div>
            <div className="p-4 bg-dark-bg rounded border border-border-subtle">
              <span className="text-text-muted block text-[10px]">PAT MARGIN</span>
              <span className="text-lg font-bold text-accent-emerald">8.6%</span>
            </div>
            <div className="p-4 bg-dark-bg rounded border border-border-subtle">
              <span className="text-text-muted block text-[10px]">EBITDA MARGIN</span>
              <span className="text-lg font-bold text-white">13.1%</span>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'swot' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="p-4 sm:p-6 bg-card-bg border border-border-strong rounded-lg space-y-2">
            <h4 className="font-bold text-accent-emerald text-sm flex items-center gap-1.5">
              <CheckCircle className="w-4 h-4" /> Key Strengths
            </h4>
            <ul className="text-xs text-text-secondary space-y-1.5 list-disc pl-4">
              <li>Market leader in urban fulfillment logistics</li>
              <li>Strong private label margin monetization</li>
            </ul>
          </div>

          <div className="p-4 sm:p-6 bg-card-bg border border-border-strong rounded-lg space-y-2">
            <h4 className="font-bold text-red-400 text-sm flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4" /> Risk Factors
            </h4>
            <ul className="text-xs text-text-secondary space-y-1.5 list-disc pl-4">
              <li>Fuel inflation impact on delivery costs</li>
              <li>Gig worker regulatory changes</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
