'use client';

import { useState } from 'react';
import { Layers, FileText, Database, ShieldAlert, Check, ChevronRight, Settings } from 'lucide-react';

export default function ReportsSettings() {
  const [activeTab, setActiveTab] = useState<'reports' | 'settings'>('reports');
  const [saved, setSaved] = useState(false);

  const [aiModel, setAiModel] = useState('GPT-4o');
  const [maxTokens, setMaxTokens] = useState(4096);
  const [apiKey, setApiKey] = useState('sk-proj-••••••••••••••••••••');

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const handleExport = (reportType: string, format: string) => {
    alert(`Exporting ${reportType} report in ${format} format...`);
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Reports & System Settings</h1>
        <p className="text-xs text-text-muted">Download platform log metrics and configure backend model parameters.</p>
      </div>

      {saved && (
        <div className="p-3 bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald rounded-md text-xs flex items-center gap-2">
          <Check className="w-4 h-4" /> System options updated successfully!
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b border-border-strong gap-8 text-sm font-semibold">
        <button
          onClick={() => setActiveTab('reports')}
          className={`pb-3 border-b-2 transition-all ${
            activeTab === 'reports' ? 'border-primary-blue text-primary-blue' : 'border-transparent text-text-muted hover:text-white'
          }`}
        >
          System Reports & Exports
        </button>
        <button
          onClick={() => setActiveTab('settings')}
          className={`pb-3 border-b-2 transition-all ${
            activeTab === 'settings' ? 'border-primary-blue text-primary-blue' : 'border-transparent text-text-muted hover:text-white'
          }`}
        >
          Model & API Settings
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {activeTab === 'reports' ? (
          /* Reports Tab */
          <div className="lg:col-span-12 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                { name: 'Revenue Reports', desc: 'Billed invoices log, plan subscriptions, and refund metrics summaries.' },
                { name: 'User Engagement Logs', desc: 'Metrics tracking active hours, dashboard visits, and watchlist actions.' },
                { name: 'AI Score Accuracy Index', desc: 'Relative comparative ratings tracking predicted listings vs. actual listing gains.' }
              ].map((rep, idx) => (
                <div key={idx} className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between h-56 hover:border-border-subtle transition-all">
                  <div className="space-y-3">
                    <FileText className="w-6 h-6 text-primary-blue" />
                    <h3 className="font-bold text-white text-sm">{rep.name}</h3>
                    <p className="text-xs text-text-secondary leading-relaxed">{rep.desc}</p>
                  </div>
                  
                  <div className="flex gap-2 border-t border-border-subtle/25 pt-4 mt-4">
                    <button onClick={() => handleExport(rep.name, 'PDF')} className="flex-1 py-1.5 rounded bg-dark-bg border border-border-subtle hover:text-white text-[10px] font-semibold text-text-secondary transition-colors">
                      PDF
                    </button>
                    <button onClick={() => handleExport(rep.name, 'Excel')} className="flex-1 py-1.5 rounded bg-dark-bg border border-border-subtle hover:text-white text-[10px] font-semibold text-text-secondary transition-colors">
                      Excel
                    </button>
                    <button onClick={() => handleExport(rep.name, 'CSV')} className="flex-1 py-1.5 rounded bg-dark-bg border border-border-subtle hover:text-white text-[10px] font-semibold text-text-secondary transition-colors">
                      CSV
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : (
          /* Settings Tab */
          <>
            <div className="lg:col-span-8 bg-card-bg border border-border-strong rounded-lg p-6 space-y-6">
              <h3 className="font-bold text-white text-sm border-b border-border-strong pb-3">OpenAI Models & API Parameters</h3>

              <div className="space-y-6 text-xs text-text-secondary">
                <div className="grid grid-cols-2 gap-6">
                  <div className="space-y-1.5">
                    <label className="font-bold text-text-muted uppercase">AI Model Selection</label>
                    <select
                      value={aiModel}
                      onChange={(e) => setAiModel(e.target.value)}
                      className="w-full h-10 px-4 rounded bg-dark-bg border border-border-subtle focus:outline-none text-text-secondary focus:border-primary-blue font-mono"
                    >
                      <option>GPT-4o</option>
                      <option>GPT-4-turbo</option>
                      <option>GPT-3.5-turbo</option>
                    </select>
                  </div>
                  <div className="space-y-1.5">
                    <label className="font-bold text-text-muted uppercase">Max Output Tokens</label>
                    <input
                      type="number"
                      value={maxTokens}
                      onChange={(e) => setMaxTokens(Number(e.target.value))}
                      className="w-full h-10 px-4 rounded bg-dark-bg border border-border-subtle focus:outline-none text-white focus:border-primary-blue font-mono"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="font-bold text-text-muted uppercase">API Authorization Key</label>
                  <input
                    type="text"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    className="w-full h-10 px-4 rounded bg-dark-bg border border-border-subtle focus:outline-none text-white focus:border-primary-blue font-mono"
                  />
                </div>

                <div className="flex justify-end pt-4 border-t border-border-subtle/25">
                  <button onClick={handleSave} className="bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs px-5 py-2.5 rounded-md shadow-md transition-colors">
                    Save Config
                  </button>
                </div>
              </div>
            </div>

            {/* Backups Panel */}
            <div className="lg:col-span-4 bg-card-bg border border-border-strong rounded-lg p-6 flex flex-col justify-between h-64">
              <div className="space-y-3">
                <h3 className="font-bold text-white text-sm flex items-center gap-2 border-b border-border-strong pb-3">
                  <Database className="w-4 h-4 text-primary-blue" /> Security & Backups
                </h3>
                <p className="text-xs text-text-secondary leading-relaxed">
                  Trigger manual data snapshots for user profiles and active IPO listing directories. Snapshots are stored in AWS S3 buckets.
                </p>
              </div>

              <button
                onClick={() => alert('Manual data backup snapshot triggered.')}
                className="w-full h-10 border border-border-subtle hover:bg-dark-bg text-xs font-semibold text-white rounded transition-colors flex items-center justify-center gap-2"
              >
                Trigger Snapshot Backup
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
