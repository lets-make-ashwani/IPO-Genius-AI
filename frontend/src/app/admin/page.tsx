'use client';

import Link from 'next/link';
import { 
  Users, 
  DollarSign, 
  Sparkles, 
  FolderOpen, 
  Activity, 
  ArrowRight,
  TrendingUp,
  Cpu,
  Database,
  Network
} from 'lucide-react';
import { mockUsers, mockIPOs } from '../../constants/mockData';

export default function AdminDashboard() {
  const latestUsers = mockUsers.slice(0, 3);
  const latestIPOs = mockIPOs.slice(0, 3);

  return (
    <div className="space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Admin Console</h1>
        <p className="text-xs text-text-muted">Manage IPO Genius AI users, listing pipelines, and engines.</p>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Total Users', val: '45,204', desc: '+12% MoM', icon: Users, trend: 'up' },
          { label: 'Active Sessions', val: '18,490', desc: '40.9% activity', icon: Activity, trend: 'neutral' },
          { label: 'Premium Subs', val: '8,340', desc: 'Pro Plan accounts', icon: Users, trend: 'up' },
          { label: 'Cumulative Revenue', val: '₹41.6L', desc: '+18.4% billing', icon: DollarSign, trend: 'up' }
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between hover:border-border-subtle transition-all">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">{card.label}</span>
                  <span className="text-3xl font-extrabold text-white font-mono">{card.val}</span>
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

      {/* Charts 2x2 Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* User Growth */}
        <div className="p-6 bg-card-bg border border-border-strong rounded-lg">
          <h3 className="font-bold text-white text-sm mb-4">User Registration Growth</h3>
          <div className="h-40 w-full bg-dark-bg/60 border border-border-subtle rounded-md flex items-end p-4 relative overflow-hidden">
            <svg className="w-full h-full overflow-visible" viewBox="0 0 100 30" preserveAspectRatio="none">
              <path d="M 0 30 Q 20 20 40 18 T 80 8 T 100 2 L 100 30 L 0 30 Z" fill="rgba(37, 99, 235, 0.15)" />
              <path d="M 0 30 Q 20 20 40 18 T 80 8 T 100 2" fill="none" stroke="#2563eb" strokeWidth="1.5" />
            </svg>
            <span className="absolute top-4 left-4 text-xs font-bold text-white font-mono">+12% growth</span>
          </div>
        </div>

        {/* Revenue */}
        <div className="p-6 bg-card-bg border border-border-strong rounded-lg">
          <h3 className="font-bold text-white text-sm mb-4">Monthly Revenue Collections</h3>
          <div className="h-40 w-full bg-dark-bg/60 border border-border-subtle rounded-md flex items-end p-4 relative overflow-hidden">
            <svg className="w-full h-full overflow-visible" viewBox="0 0 100 30" preserveAspectRatio="none">
              {/* Simplistic bar representation */}
              <rect x="5" y="10" width="8" height="20" fill="#2563eb" rx="1" />
              <rect x="20" y="15" width="8" height="15" fill="#2563eb" rx="1" />
              <rect x="35" y="8" width="8" height="22" fill="#2563eb" rx="1" />
              <rect x="50" y="12" width="8" height="18" fill="#2563eb" rx="1" />
              <rect x="65" y="5" width="8" height="25" fill="#2563eb" rx="1" />
              <rect x="80" y="2" width="8" height="28" fill="#7c3aed" rx="1" />
            </svg>
            <span className="absolute top-4 left-4 text-xs font-bold text-white font-mono">₹41,61,660 Current</span>
          </div>
        </div>
      </div>

      {/* Bottom Layout columns */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Side: Tables */}
        <div className="lg:col-span-8 space-y-8">
          {/* Latest Users */}
          <div className="bg-card-bg border border-border-strong rounded-lg overflow-hidden">
            <div className="p-4 border-b border-border-strong bg-dark-bg/25 flex justify-between items-center">
              <h3 className="font-bold text-white text-sm">Latest User Registrations</h3>
              <Link href="/admin/users" className="text-xs font-semibold text-primary-blue hover:underline">Manage Users</Link>
            </div>
            <div className="divide-y divide-border-strong/30">
              {latestUsers.map((u) => (
                <div key={u.id} className="flex justify-between items-center p-4 text-xs">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-primary-blue/20 flex items-center justify-center font-bold text-primary-blue">{u.avatar}</div>
                    <div>
                      <span className="font-bold text-white block">{u.name}</span>
                      <span className="text-[10px] text-text-muted">{u.email}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="text-[10px] font-bold text-text-secondary bg-dark-bg border border-border-subtle/50 px-2 py-0.5 rounded">{u.plan}</span>
                    <span className="text-text-muted font-mono">{u.joinedDate}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Latest IPOs */}
          <div className="bg-card-bg border border-border-strong rounded-lg overflow-hidden">
            <div className="p-4 border-b border-border-strong bg-dark-bg/25 flex justify-between items-center">
              <h3 className="font-bold text-white text-sm">Latest System IPOs</h3>
              <Link href="/admin/ipo" className="text-xs font-semibold text-primary-blue hover:underline">Manage IPOs</Link>
            </div>
            <div className="divide-y divide-border-strong/30">
              {latestIPOs.map((ipo) => (
                <div key={ipo.id} className="flex justify-between items-center p-4 text-xs">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded bg-primary-blue/10 flex items-center justify-center font-bold text-primary-blue font-mono">{ipo.ticker.substring(0, 2)}</div>
                    <div>
                      <span className="font-bold text-white block">{ipo.name}</span>
                      <span className="text-[10px] text-text-muted">{ipo.ticker}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
                      ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' : 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20'
                    }`}>{ipo.status.toUpperCase()}</span>
                    <div className="w-6 h-6 rounded-full bg-accent-emerald/10 text-accent-emerald flex items-center justify-center font-bold font-mono">{ipo.aiScore}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Side: System Status */}
        <div className="lg:col-span-4 space-y-6">
          <div className="p-6 bg-card-bg border border-border-strong rounded-lg space-y-6">
            <h3 className="font-bold text-white text-sm flex items-center gap-2 border-b border-border-strong pb-3">
              <Cpu className="w-4 h-4 text-primary-blue" /> Engine Health status
            </h3>

            <div className="space-y-4 text-xs">
              {[
                { label: 'PostgreSQL Database', stat: 'ONLINE', success: true },
                { label: 'FastAPI Backend Core', stat: 'ONLINE', success: true },
                { label: 'n8n Automation Engine', stat: 'ONLINE', success: true },
                { label: 'OpenAI API Node', stat: 'ONLINE', success: true }
              ].map((row, idx) => (
                <div key={idx} className="flex justify-between items-center">
                  <span className="text-text-secondary">{row.label}</span>
                  <span className={`text-[9px] font-bold px-2 py-0.5 rounded-sm ${
                    row.success ? 'bg-accent-emerald/20 text-accent-emerald' : 'bg-red-500/20 text-red-400'
                  }`}>{row.stat}</span>
                </div>
              ))}
            </div>

            <div className="pt-4 border-t border-border-subtle/25 space-y-2">
              <span className="text-[10px] text-text-muted block">AI ANALYSIS QUEUE</span>
              <div className="flex justify-between text-[10px] font-semibold text-text-secondary">
                <span>Pending Jobs</span>
                <span className="font-mono">0 / 0</span>
              </div>
              <div className="w-full h-1.5 bg-dark-bg rounded-full overflow-hidden">
                <div className="h-full bg-accent-emerald rounded-full" style={{ width: '0%' }} />
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
