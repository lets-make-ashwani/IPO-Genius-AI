'use client';

import Link from 'next/link';
import { 
  TrendingUp, 
  TrendingDown, 
  Sparkles, 
  Calendar, 
  Circle, 
  BarChart3, 
  AlertTriangle,
  ArrowRight,
  Star,
  Bell
} from 'lucide-react';
import { mockIPOs } from '../../constants/mockData';

export default function DashboardHome() {
  const trendingIPOs = mockIPOs.slice(0, 3);

  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Good morning, Rahul 👋</h1>
          <p className="text-xs text-text-muted">Here's your IPO market activity recap for today.</p>
        </div>
        <span className="text-xs font-semibold text-text-muted font-mono bg-card-bg border border-border-strong px-3 py-1.5 rounded-md">
          {new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </span>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Total IPOs', val: '248', desc: '+12 this month', icon: BarChart3, iconColor: 'text-primary-blue bg-primary-blue/10', trend: 'up' },
          { label: 'Currently Open', val: '8', desc: '3 closing soon', icon: Circle, iconColor: 'text-accent-emerald bg-accent-emerald/10', trend: 'warning' },
          { label: 'Opening Soon', val: '15', desc: 'Next: 18 July', icon: Calendar, iconColor: 'text-secondary-purple bg-secondary-purple/10', trend: 'neutral' },
          { label: 'Average Listing Gain', val: '+24.6%', desc: 'Based on 47 deals', icon: TrendingUp, iconColor: 'text-accent-emerald bg-accent-emerald/10', trend: 'up' }
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between hover:border-border-subtle transition-all">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">{card.label}</span>
                  <span className="text-3xl font-extrabold text-white font-mono">{card.val}</span>
                </div>
                <div className={`p-2.5 rounded-md ${card.iconColor}`}>
                  <Icon className="w-5 h-5" />
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-border-subtle/30 flex items-center gap-1.5 text-xs text-text-secondary">
                {card.trend === 'up' && <TrendingUp className="w-3.5 h-3.5 text-accent-emerald" />}
                {card.trend === 'warning' && <AlertTriangle className="w-3.5 h-3.5 text-yellow-500" />}
                <span className={
                  card.trend === 'up' ? 'text-accent-emerald font-semibold' :
                  card.trend === 'warning' ? 'text-yellow-500 font-semibold' : 'text-text-muted'
                }>{card.desc}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Primary Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Market Overview Chart Placeholder */}
        <div className="lg:col-span-8 bg-card-bg border border-border-strong rounded-lg p-6 flex flex-col justify-between">
          <div>
            <div className="flex justify-between items-center mb-6">
              <h3 className="font-bold text-white text-base">Market Overview</h3>
              <div className="flex gap-2 text-xs font-semibold">
                <span className="px-2 py-1 rounded bg-primary-blue text-white cursor-pointer">7D</span>
                <span className="px-2 py-1 rounded bg-dark-bg text-text-muted hover:text-white cursor-pointer">30D</span>
                <span className="px-2 py-1 rounded bg-dark-bg text-text-muted hover:text-white cursor-pointer">1Y</span>
              </div>
            </div>

            {/* Simple Inline SVG Sparkline representation for rendering safety */}
            <div className="h-48 w-full bg-dark-bg/60 border border-border-subtle rounded-md flex items-end p-4 relative overflow-hidden">
              <svg className="w-full h-full overflow-visible" viewBox="0 0 100 30" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="chart-glow" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#2563eb" stopOpacity="0.4"/>
                    <stop offset="100%" stopColor="#2563eb" stopOpacity="0"/>
                  </linearGradient>
                </defs>
                <path d="M 0 25 Q 15 10 30 20 T 60 12 T 90 2 Q 95 1 100 8 L 100 30 L 0 30 Z" fill="url(#chart-glow)" />
                <path d="M 0 25 Q 15 10 30 20 T 60 12 T 90 2 Q 95 1 100 8" fill="none" stroke="#2563eb" strokeWidth="1.5" />
              </svg>
              <div className="absolute top-4 left-4 flex gap-4 text-xs font-mono">
                <div>
                  <span className="text-[10px] text-text-muted block">TOTAL VOLUME</span>
                  <span className="font-bold text-white">₹2,450 Cr</span>
                </div>
                <div>
                  <span className="text-[10px] text-text-muted block">AVG GMP GAIN</span>
                  <span className="font-bold text-accent-emerald">+24.6%</span>
                </div>
              </div>
            </div>
          </div>
          <p className="text-[10px] text-text-muted mt-4">Graph shows cumulative pricing GMP indices and activity indexes over selected timeline.</p>
        </div>

        {/* AI Pick card */}
        <div className="lg:col-span-4 bg-card-bg border border-border-strong rounded-lg p-6 flex flex-col justify-between relative overflow-hidden animate-pulse-glow">
          <div className="absolute top-0 right-0 -translate-y-8 translate-x-8 w-24 h-24 bg-secondary-purple/10 rounded-full blur-[40px]" />
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold text-secondary-purple mb-4">
              <Sparkles className="w-4 h-4" />
              <span>AI PICK OF THE DAY</span>
            </div>
            
            <h3 className="text-xl font-bold text-white mb-1">Swiggy Ltd</h3>
            <span className="text-xs text-text-muted block mb-6">Food Delivery & Quick Commerce</span>

            <div className="flex items-center gap-4 bg-dark-bg border border-border-subtle p-4 rounded-lg mb-6">
              <div className="w-14 h-14 rounded-full border-4 border-accent-emerald flex items-center justify-center font-bold text-accent-emerald text-base font-mono">
                87
              </div>
              <div>
                <span className="text-[10px] font-bold text-accent-emerald bg-accent-emerald/10 border border-accent-emerald/20 px-2 py-0.5 rounded-sm block w-fit mb-1">STRONG BUY</span>
                <span className="text-xs text-text-secondary leading-tight block">High confidence score driven by margin improvements.</span>
              </div>
            </div>
          </div>

          <Link href="/dashboard/ipo/swiggy" className="w-full h-10 rounded-md bg-secondary-purple hover:bg-purple-700 text-white font-semibold text-sm transition-colors flex items-center justify-center gap-2">
            View AI Analysis <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* Trending IPOs */}
      <div className="space-y-6">
        <div className="flex justify-between items-end border-b border-border-strong pb-3">
          <h3 className="font-bold text-white text-base">Trending IPOs</h3>
          <Link href="/dashboard/ipo" className="text-xs font-semibold text-primary-blue hover:underline">
            View All IPOs
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {trendingIPOs.map((ipo) => (
            <div key={ipo.id} className="p-6 rounded-lg bg-card-bg border border-border-strong hover:border-primary-blue/30 transition-all flex flex-col justify-between h-96">
              <div>
                <div className="flex items-center justify-between mb-6">
                  <div className="w-10 h-10 rounded-md bg-gradient-to-br from-primary-blue/10 to-secondary-purple/10 flex items-center justify-center font-bold text-primary-blue font-mono">
                    {ipo.name.charAt(0)}
                  </div>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                    ipo.status === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20' :
                    'bg-red-500/10 text-red-400 border border-red-500/20'
                  }`}>
                    {ipo.status.toUpperCase()}
                  </span>
                </div>
                
                <h3 className="text-base font-bold text-white mb-1">{ipo.name}</h3>
                <span className="text-xs text-text-muted">{ipo.sector}</span>
                
                <div className="grid grid-cols-2 gap-4 mt-6 text-xs border-t border-border-subtle/40 pt-4">
                  <div>
                    <span className="text-text-muted block mb-0.5">PRICE BAND</span>
                    <span className="font-bold text-white font-mono">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</span>
                  </div>
                  <div>
                    <span className="text-text-muted block mb-0.5">ISSUE SIZE</span>
                    <span className="font-bold text-white font-mono">₹{ipo.issueSize} Cr</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between border-t border-border-subtle/40 pt-4 mt-6">
                <div className="flex items-center gap-2">
                  <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center font-bold text-xs ${
                    ipo.aiScore >= 80 ? 'border-accent-emerald text-accent-emerald' : 'border-yellow-500 text-yellow-500'
                  }`}>
                    {ipo.aiScore}
                  </div>
                  <div className="text-left leading-none">
                    <span className="text-[9px] text-text-muted block">AI SCORE</span>
                    <span className="text-[10px] font-bold text-white">{ipo.aiRecommendation}</span>
                  </div>
                </div>
                <Link href={`/dashboard/ipo/${ipo.id}`} className="text-xs font-semibold bg-border-subtle hover:bg-border-strong text-white px-3.5 py-2 rounded-md transition-colors">
                  Details →
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Grid: Watchlist & Notifications */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Watchlist Preview */}
        <div className="p-6 bg-card-bg border border-border-strong rounded-lg">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-bold text-white text-base">Watchlist Preview</h3>
            <Link href="/dashboard/watchlist" className="text-xs font-semibold text-primary-blue hover:underline">View Watchlist</Link>
          </div>
          <div className="space-y-4">
            {trendingIPOs.map((ipo) => (
              <div key={ipo.id} className="flex justify-between items-center p-3 rounded bg-dark-bg/60 border border-border-subtle">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded bg-primary-blue/10 flex items-center justify-center font-bold text-primary-blue text-sm font-mono">
                    {ipo.ticker.substring(0, 2)}
                  </div>
                  <div className="text-left">
                    <h5 className="text-xs font-bold text-white leading-tight">{ipo.name}</h5>
                    <span className="text-[10px] text-text-muted">{ipo.ticker}</span>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-xs font-mono font-bold text-white">GMP +{ipo.gmp}%</span>
                  <div className="w-7 h-7 rounded-full bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald font-bold text-xs flex items-center justify-center font-mono">
                    {ipo.aiScore}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Notifications Preview */}
        <div className="p-6 bg-card-bg border border-border-strong rounded-lg">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-bold text-white text-base">Latest Alerts</h3>
            <Link href="/dashboard/notifications" className="text-xs font-semibold text-primary-blue hover:underline">Mark all read</Link>
          </div>
          <div className="space-y-4">
            <div className="p-3 bg-blue-600/5 border-l-2 border-primary-blue rounded flex gap-3 text-xs">
              <Bell className="w-4 h-4 text-primary-blue shrink-0 mt-0.5" />
              <div>
                <p className="text-white font-semibold mb-1">Swiggy IPO opens tomorrow!</p>
                <span className="text-[10px] text-text-muted">2 hours ago</span>
              </div>
            </div>
            <div className="p-3 bg-emerald-500/5 border-l-2 border-accent-emerald rounded flex gap-3 text-xs">
              <TrendingUp className="w-4 h-4 text-accent-emerald shrink-0 mt-0.5" />
              <div>
                <p className="text-white font-semibold mb-1">Bajaj Housing listed at +110% profit!</p>
                <span className="text-[10px] text-text-muted">1 day ago</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
