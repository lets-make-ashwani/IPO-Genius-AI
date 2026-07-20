'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Users, 
  DollarSign, 
  Sparkles, 
  Activity, 
  ArrowRight,
  TrendingUp,
  Database,
  CheckCircle,
  Play
} from 'lucide-react';
import { ipoService } from '../../services/ipo.service';
import { IPO } from '../../types';

export default function AdminDashboard() {
  const [latestIPOs, setLatestIPOs] = useState<IPO[]>([]);
  const [totalIPOs, setTotalIPOs] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    ipoService.getIPOs(undefined, undefined, undefined, undefined, 1, 5)
      .then(res => {
        if (isMounted) {
          setLatestIPOs(res.items);
          setTotalIPOs(res.total);
          setLoading(false);
        }
      })
      .catch(err => {
        console.error('Failed to load admin stats:', err);
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Admin Console & Enterprise Control</h1>
          <p className="text-xs text-text-muted">Live pipeline orchestration, database management, and engine health.</p>
        </div>
        <span className="text-xs font-mono bg-card-bg border border-border-strong px-3 py-1.5 rounded text-accent-emerald flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-accent-emerald animate-ping" /> System Online
        </span>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Database IPO Records', val: totalIPOs, desc: 'Live DB persisted', icon: Database, trend: 'up' },
          { label: 'Active Pipeline Scrapers', val: '5 / 5', desc: 'NSE, BSE, InvestorGain, Chittorgarh, SEBI', icon: Activity, trend: 'neutral' },
          { label: 'AI Analyses Generated', val: totalIPOs, desc: 'Gemini 1.5 Flash', icon: Sparkles, trend: 'up' },
          { label: 'API Contract Version', val: 'v1.0.0', desc: 'FastAPI Production SLA', icon: Users, trend: 'up' }
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between hover:border-border-subtle transition-all">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">{card.label}</span>
                  <span className="text-3xl font-extrabold text-white font-mono">{loading ? '...' : card.val}</span>
                </div>
                <div className="p-2.5 rounded-md bg-dark-bg/60 text-primary-blue">
                  <Icon className="w-5 h-5" />
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-border-subtle/30 flex items-center gap-1.5 text-xs text-text-secondary">
                {card.trend === 'up' && <TrendingUp className="w-3.5 h-3.5 text-accent-emerald" />}
                <span className={card.trend === 'up' ? 'text-accent-emerald font-semibold' : 'text-text-muted'}>{card.desc}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Action Navigation Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link href="/admin/ipo" className="p-6 bg-card-bg border border-border-strong rounded-lg hover:border-primary-blue/40 transition-all flex justify-between items-center group">
          <div>
            <h3 className="font-bold text-white text-base group-hover:text-primary-blue transition-colors">IPO Deal Management</h3>
            <p className="text-xs text-text-muted mt-1">Create, edit, delete, or trigger Gemini AI evaluation for IPOs.</p>
          </div>
          <ArrowRight className="w-5 h-5 text-text-muted group-hover:text-primary-blue group-hover:translate-x-1 transition-all" />
        </Link>

        <Link href="/admin/automation" className="p-6 bg-card-bg border border-border-strong rounded-lg hover:border-secondary-purple/40 transition-all flex justify-between items-center group">
          <div>
            <h3 className="font-bold text-white text-base group-hover:text-secondary-purple transition-colors">Automation Pipeline</h3>
            <p className="text-xs text-text-muted mt-1">Run manual scrapers, view execution logs, or pause APScheduler.</p>
          </div>
          <Play className="w-5 h-5 text-text-muted group-hover:text-secondary-purple group-hover:translate-x-1 transition-all" />
        </Link>

        <Link href="/admin/users" className="p-6 bg-card-bg border border-border-strong rounded-lg hover:border-accent-emerald/40 transition-all flex justify-between items-center group">
          <div>
            <h3 className="font-bold text-white text-base group-hover:text-accent-emerald transition-colors">User Management</h3>
            <p className="text-xs text-text-muted mt-1">Audit accounts, manage RBAC permissions, and view user logs.</p>
          </div>
          <Users className="w-5 h-5 text-text-muted group-hover:text-accent-emerald group-hover:translate-x-1 transition-all" />
        </Link>
      </div>

      {/* Latest Persisted Database Records Table */}
      <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-bold text-white text-base flex items-center gap-2">
            <Database className="w-4 h-4 text-primary-blue" /> Live Database IPO Records
          </h3>
          <Link href="/admin/ipo" className="text-xs font-semibold text-primary-blue hover:underline">
            Manage All →
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-dark-bg/60 text-text-muted uppercase text-[10px] font-mono border-b border-border-subtle">
              <tr>
                <th className="p-3">Company Name</th>
                <th className="p-3">Status</th>
                <th className="p-3">Price Band</th>
                <th className="p-3">Lot Size</th>
                <th className="p-3">Exchange</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle/40 text-text-secondary font-mono">
              {latestIPOs.map((ipo) => (
                <tr key={ipo.id} className="hover:bg-dark-bg/30 transition-colors">
                  <td className="p-3 font-semibold text-white font-sans">{ipo.name}</td>
                  <td className="p-3">
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20">
                      {ipo.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="p-3">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</td>
                  <td className="p-3">{ipo.lotSize}</td>
                  <td className="p-3">BSE & NSE</td>
                  <td className="p-3 text-right font-sans">
                    <Link href={`/dashboard/ipo/${ipo.id}`} className="text-primary-blue hover:underline font-semibold">
                      View Live →
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
