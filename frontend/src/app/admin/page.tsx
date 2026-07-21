'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Users, 
  Sparkles, 
  Activity, 
  ArrowRight,
  TrendingUp,
  Database,
  RotateCcw,
  ShieldCheck
} from 'lucide-react';
import { ipoService } from '../../services/ipo.service';
import { apiClient } from '../../api/client';
import { IPO } from '../../types';

export default function AdminDashboard() {
  const [latestIPOs, setLatestIPOs] = useState<IPO[]>([]);
  const [totalIPOs, setTotalIPOs] = useState(0);
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const loadAdminData = () => {
    setLoading(true);
    ipoService.getIPOs(undefined, undefined, undefined, undefined, 1, 5)
      .then(res => {
        setLatestIPOs(res.items);
        setTotalIPOs(res.total);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load admin stats:', err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadAdminData();
  }, []);

  const handleInitDatabase = async () => {
    setIsProcessing(true);
    setActionMessage(null);
    try {
      await apiClient.post('/admin/database/seed', {});
      setActionMessage('Database Initialized & Seeded Successfully! Refreshing...');
      setTimeout(() => {
        loadAdminData();
        setIsProcessing(false);
      }, 2000);
    } catch (err: any) {
      setActionMessage(`Error initializing database: ${err.message || 'Server error'}`);
      setIsProcessing(false);
    }
  };

  const handleReseedDatabase = async () => {
    if (!confirm('SUPER ADMIN WARNING: Are you sure you want to force reseed and re-evaluate the initial dataset?')) return;
    setIsProcessing(true);
    setActionMessage(null);
    try {
      await apiClient.post('/admin/database/reseed', { confirm: true });
      setActionMessage('Database Force Reseed Completed & AI Generation Queued!');
      setTimeout(() => {
        loadAdminData();
        setIsProcessing(false);
      }, 2000);
    } catch (err: any) {
      setActionMessage(`Error reseeding database: ${err.message || 'Server error'}`);
      setIsProcessing(false);
    }
  };

  return (
    <div className="space-y-6 sm:space-y-8 max-w-full overflow-x-hidden">
      {/* Title */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-white mb-1">Admin Console & Enterprise Control</h1>
          <p className="text-xs text-text-muted">Live pipeline orchestration, database management, and engine health.</p>
        </div>
        <div className="flex flex-wrap items-center gap-2.5 w-full sm:w-auto">
          <button
            onClick={handleInitDatabase}
            disabled={isProcessing}
            className="bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs px-3.5 py-2 rounded-md flex items-center gap-1.5 transition-all disabled:opacity-50 min-h-[44px]"
          >
            <Database className="w-4 h-4" />
            Initialize Database
          </button>
          <button
            onClick={handleReseedDatabase}
            disabled={isProcessing}
            className="bg-dark-bg hover:bg-card-bg border border-border-subtle hover:border-red-400/50 text-red-400 font-semibold text-xs px-3.5 py-2 rounded-md flex items-center gap-1.5 transition-all disabled:opacity-50 min-h-[44px]"
          >
            <RotateCcw className="w-4 h-4" />
            Force Reseed
          </button>
        </div>
      </div>

      {actionMessage && (
        <div className="p-4 rounded-md bg-primary-blue/10 border border-primary-blue/30 text-xs text-primary-blue font-semibold">
          {actionMessage}
        </div>
      )}

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 min-[480px]:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'PERSISTED DEALS', val: totalIPOs, desc: 'Real database records', icon: Database },
          { label: 'SCRAPER PIPELINES', val: 'Active', desc: 'NSE, BSE, Chittorgarh', icon: Activity },
          { label: 'AI EVALUATIONS', val: '100%', desc: 'Gemini 1.5 Flash', icon: Sparkles },
          { label: 'REGISTERED USERS', val: '1', desc: 'Super Admin', icon: Users },
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="p-4 sm:p-5 bg-card-bg border border-border-strong rounded-lg flex justify-between items-center">
              <div>
                <span className="text-[10px] sm:text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">{card.label}</span>
                <span className="text-xl sm:text-2xl font-bold text-white font-mono">{loading ? '...' : card.val}</span>
                <span className="text-[10px] text-text-muted block mt-1">{card.desc}</span>
              </div>
              <Icon className="w-6 h-6 text-primary-blue/30 shrink-0" />
            </div>
          );
        })}
      </div>

      {/* Latest Database Records Table & Mobile Cards */}
      <div className="p-4 sm:p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="font-bold text-white text-base">Latest Persisted Database Records</h2>
          <Link href="/admin/ipo" className="text-xs font-semibold text-primary-blue hover:underline flex items-center gap-1 min-h-[44px]">
            Manage All →
          </Link>
        </div>

        {/* Mobile Stacked Card View */}
        <div className="grid grid-cols-1 md:hidden gap-3">
          {latestIPOs.map((ipo) => (
            <div key={ipo.id} className="p-4 bg-dark-bg border border-border-subtle rounded-lg space-y-2">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-bold text-white text-sm break-words">{ipo.name}</h3>
                  <span className="text-[11px] text-text-muted font-mono">{ipo.sector}</span>
                </div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20">
                  {ipo.status}
                </span>
              </div>
              <div className="flex justify-between text-xs font-mono pt-2 border-t border-border-subtle/40">
                <span className="text-text-muted">Price: ₹{ipo.priceBand.min}-₹{ipo.priceBand.max}</span>
                <span className="text-accent-emerald">GMP: +{ipo.gmp}%</span>
              </div>
            </div>
          ))}
        </div>

        {/* Desktop HTML Table */}
        <div className="hidden md:block overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-border-subtle text-text-muted uppercase text-[10px] font-mono">
                <th className="p-3">Company Name</th>
                <th className="p-3">Status</th>
                <th className="p-3">Price Band</th>
                <th className="p-3">GMP</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle/40 font-mono text-text-secondary">
              {latestIPOs.map((ipo) => (
                <tr key={ipo.id} className="hover:bg-dark-bg/30">
                  <td className="p-3 font-sans font-semibold text-white">{ipo.name}</td>
                  <td className="p-3">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20">
                      {ipo.status}
                    </span>
                  </td>
                  <td className="p-3">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</td>
                  <td className="p-3 text-accent-emerald">+{ipo.gmp}%</td>
                  <td className="p-3 text-right font-sans">
                    <Link href={`/dashboard/ipo/${ipo.id}`} className="text-primary-blue hover:underline font-semibold">
                      Inspect
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
