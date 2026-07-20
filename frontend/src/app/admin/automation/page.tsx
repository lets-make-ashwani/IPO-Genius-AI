'use client';

import { useState } from 'react';
import { Sparkles, Play, Activity, CheckCircle } from 'lucide-react';
import { apiClient } from '../../../api/client';

export default function AutomationControl() {
  const [runningProvider, setRunningProvider] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const scrapers = [
    { provider: 'NSE', name: 'NSE India Official IPO API Scraper', description: 'Fetches active, upcoming, and listed deals from nseindia.com API endpoints.' },
    { provider: 'BSE', name: 'BSE India Primary Market Scraper', description: 'Parses equity issue listings, price bands, and lot sizes from bseindia.com.' },
    { provider: 'InvestorGain', name: 'InvestorGain Live GMP Collector', description: 'Scrapes Grey Market Premium (GMP) updates and expected listing gains.' },
    { provider: 'Chittorgarh', name: 'Chittorgarh Subscription Tracker', description: 'Extracts real-time QIB, NII, Retail, and total subscription multiples.' },
    { provider: 'SEBI', name: 'SEBI DRHP & RHP Regulatory Parser', description: 'Fetches draft prospectus PDF filings and extracts financial overview tables.' }
  ];

  const handleRunScraper = async (provider: string) => {
    setRunningProvider(provider);
    setMessage(null);
    try {
      await apiClient.post('/admin/pipeline/run', { provider });
      setMessage(`Master Pipeline Execution triggered for ${provider}! Output saved to database.`);
    } catch (err: any) {
      setMessage(`Error triggering ${provider}: ${err.message || 'Server error'}`);
    } finally {
      setRunningProvider(null);
    }
  };

  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Automation Scraper & Pipeline Control</h1>
          <p className="text-xs text-text-muted">Orchestrate scrapers, background job schedulers, and Gemini AI analysis.</p>
        </div>
        <span className="text-xs font-mono bg-card-bg border border-border-strong px-3 py-1 rounded text-accent-emerald flex items-center gap-1.5">
          <Activity className="w-4 h-4 text-accent-emerald animate-pulse" /> Schedulers Running
        </span>
      </div>

      {message && (
        <div className="p-4 bg-secondary-purple/10 border border-secondary-purple/30 rounded-lg text-xs text-secondary-purple font-semibold">
          {message}
        </div>
      )}

      {/* Scraper Controls Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {scrapers.map((item) => (
          <div key={item.provider} className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between space-y-4">
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-bold text-primary-blue font-mono px-2 py-0.5 rounded bg-primary-blue/10 border border-primary-blue/20">
                  {item.provider}
                </span>
                <span className="text-[10px] text-text-muted font-mono">STATUS: ACTIVE</span>
              </div>
              <h3 className="font-bold text-white text-base">{item.name}</h3>
              <p className="text-xs text-text-secondary mt-1 leading-relaxed">{item.description}</p>
            </div>

            <button
              onClick={() => handleRunScraper(item.provider)}
              disabled={runningProvider === item.provider}
              className="w-full bg-dark-bg hover:bg-card-bg border border-border-subtle hover:border-primary-blue/40 text-white font-semibold text-xs py-2.5 rounded-md flex items-center justify-center gap-1.5 transition-all disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5 fill-white" />
              {runningProvider === item.provider ? `Executing ${item.provider}...` : `Run ${item.provider} Scraper Now`}
            </button>
          </div>
        ))}
      </div>

      {/* Pipeline State Machine Specifications */}
      <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
        <h3 className="text-white font-bold text-base flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-secondary-purple" /> 7-Stage State Machine Pipeline
        </h3>
        <p className="text-xs text-text-muted leading-relaxed">
          Every raw scraped record automatically advances through the 7-stage state machine:
          <code className="text-primary-blue font-mono block mt-2 p-2 bg-dark-bg border border-border-subtle rounded text-[11px]">
            DISCOVERY ➔ DOCUMENT_FETCH ➔ EXTRACTION ➔ NORMALIZATION ➔ VALIDATION ➔ IPO_UPSERT ➔ AI_GENERATION ➔ COMPLETED
          </code>
        </p>
      </div>
    </div>
  );
}
