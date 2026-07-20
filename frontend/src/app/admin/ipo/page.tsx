'use client';

import { useState, useEffect } from 'react';
import { 
  Plus, 
  Search, 
  Trash2, 
  Check, 
  X,
  Play,
  Sparkles,
  RefreshCw
} from 'lucide-react';
import { IPO } from '../../../types';
import { ipoService } from '../../../services/ipo.service';
import { apiClient } from '../../../api/client';

export default function IPOManagement() {
  const [ipos, setIpos] = useState<IPO[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [runningPipeline, setRunningPipeline] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const loadIPOs = () => {
    setLoading(true);
    ipoService.getIPOs(search, undefined, undefined, undefined, 1, 50)
      .then(res => {
        setIpos(res.items);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching admin IPO list:', err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadIPOs();
  }, [search]);

  const handleRunPipeline = async (provider: string = 'NSE') => {
    setRunningPipeline(true);
    setMessage(null);
    try {
      await apiClient.post('/admin/pipeline/run', { provider });
      setMessage(`Master Scraper & Gemini AI Pipeline triggered for ${provider}! Refreshing...`);
      setTimeout(() => {
        loadIPOs();
        setRunningPipeline(false);
      }, 3000);
    } catch (err: any) {
      setMessage(`Pipeline Trigger Error: ${err.message || 'Unauthorized or server error'}`);
      setRunningPipeline(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">IPO Deal & Pipeline Management</h1>
          <p className="text-xs text-text-muted">Direct control over database IPO entries, scrapers, and Gemini AI analysis.</p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => handleRunPipeline('NSE')}
            disabled={runningPipeline}
            className="bg-secondary-purple hover:bg-purple-700 disabled:opacity-50 text-white font-semibold text-xs px-4 py-2.5 rounded-md flex items-center gap-1.5 shadow-lg shadow-secondary-purple/20 transition-all"
          >
            <Play className="w-4 h-4 fill-white" />
            {runningPipeline ? 'Running Scrapers...' : 'Trigger Live Scrapers'}
          </button>
        </div>
      </div>

      {message && (
        <div className="p-3 bg-secondary-purple/10 border border-secondary-purple/30 rounded-md text-xs text-secondary-purple font-semibold">
          {message}
        </div>
      )}

      {/* Control Header */}
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 bg-card-bg border border-border-strong p-4 rounded-lg">
        <div className="relative w-full md:w-80">
          <Search className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
          <input
            type="text"
            placeholder="Filter database IPOs..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-10 pl-10 pr-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none text-white"
          />
        </div>

        <button 
          onClick={loadIPOs} 
          className="p-2.5 bg-dark-bg border border-border-subtle hover:bg-card-bg rounded-md text-text-muted hover:text-white"
          title="Refresh List"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* IPO Data Table */}
      <div className="bg-card-bg border border-border-strong rounded-lg overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-border-strong bg-dark-bg/60 text-text-muted uppercase text-[10px] font-mono">
              <th className="p-4">Company Name</th>
              <th className="p-4">Status</th>
              <th className="p-4">Price Band</th>
              <th className="p-4">Lot Size</th>
              <th className="p-4">Open Date</th>
              <th className="p-4">Close Date</th>
              <th className="p-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle/40 text-text-secondary">
            {loading ? (
              <tr>
                <td colSpan={7} className="p-8 text-center text-text-muted">Loading live database records...</td>
              </tr>
            ) : ipos.length > 0 ? (
              ipos.map((ipo) => (
                <tr key={ipo.id} className="hover:bg-dark-bg/40 transition-colors">
                  <td className="p-4 font-semibold text-white font-sans">
                    {ipo.name}
                    <span className="block text-[10px] text-text-muted font-mono">{ipo.sector}</span>
                  </td>
                  <td className="p-4">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                      ipo.status === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20' :
                      'bg-dark-bg text-text-muted border border-border-subtle'
                    }`}>
                      {ipo.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="p-4 font-mono">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</td>
                  <td className="p-4 font-mono">{ipo.lotSize}</td>
                  <td className="p-4 font-mono">{ipo.openDate}</td>
                  <td className="p-4 font-mono">{ipo.closeDate}</td>
                  <td className="p-4 text-right space-x-2">
                    <a
                      href={`/dashboard/ipo/${ipo.id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-blue hover:underline font-semibold"
                    >
                      View Live →
                    </a>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={7} className="p-8 text-center text-text-muted">No database records found matching filter.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
