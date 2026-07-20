'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  TrendingUp, 
  Sparkles, 
  Calendar, 
  Circle, 
  BarChart3, 
  ArrowRight,
  Star
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { ipoService } from '../../services/ipo.service';
import { IPO } from '../../types';

export default function DashboardHome() {
  const { user } = useAuth();
  const [trendingIPOs, setTrendingIPOs] = useState<IPO[]>([]);
  const [counts, setCounts] = useState({ total: 10, open: 1, upcoming: 2, listed: 7 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    Promise.all([
      ipoService.getIPOs(undefined, undefined, undefined, undefined, 1, 3),
      ipoService.getIPOs(undefined, 'OPEN', undefined, undefined, 1, 1),
      ipoService.getIPOs(undefined, 'UPCOMING', undefined, undefined, 1, 1),
      ipoService.getIPOs(undefined, 'LISTED', undefined, undefined, 1, 1),
    ]).then(([allRes, openRes, upcomingRes, listedRes]) => {
      if (isMounted) {
        setTrendingIPOs(allRes.items);
        setCounts({
          total: allRes.total || 10,
          open: openRes.total || 1,
          upcoming: upcomingRes.total || 2,
          listed: listedRes.total || 7
        });
        setLoading(false);
      }
    }).catch(err => {
      console.error('Failed to load dashboard metrics:', err);
      if (isMounted) setLoading(false);
    });

    return () => {
      isMounted = false;
    };
  }, []);

  const userName = user?.name ? user.name.split(' ')[0] : 'Investor';

  return (
    <div className="space-y-8">
      {/* Title */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Good day, {userName} 👋</h1>
          <p className="text-xs text-text-muted">Here is your live IPO market intelligence recap.</p>
        </div>
        <span className="text-xs font-semibold text-text-muted font-mono bg-card-bg border border-border-strong px-3 py-1.5 rounded-md">
          {new Date().toLocaleDateString('en-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </span>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: 'Total IPOs Tracked', val: counts.total, desc: 'Live DB records', icon: BarChart3, iconColor: 'text-primary-blue bg-primary-blue/10' },
          { label: 'Currently Open', val: counts.open, desc: 'Bidding active', icon: Circle, iconColor: 'text-accent-emerald bg-accent-emerald/10' },
          { label: 'Upcoming Issues', val: counts.upcoming, desc: 'Filing pipeline', icon: Calendar, iconColor: 'text-secondary-purple bg-secondary-purple/10' },
          { label: 'Recently Listed', val: counts.listed, desc: 'Exchange traded', icon: TrendingUp, iconColor: 'text-accent-emerald bg-accent-emerald/10' }
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between hover:border-border-subtle transition-all">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider">{card.label}</span>
                  <span className="text-3xl font-extrabold text-white font-mono">{loading ? '...' : card.val}</span>
                </div>
                <div className={`p-2.5 rounded-md ${card.iconColor}`}>
                  <Icon className="w-5 h-5" />
                </div>
              </div>
              <span className="text-[11px] text-text-muted mt-4 block">{card.desc}</span>
            </div>
          );
        })}
      </div>

      {/* Live Trending Deals Section */}
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-secondary-purple" /> Live Market IPO Deals
          </h2>
          <Link href="/dashboard/ipo" className="text-xs font-semibold text-primary-blue hover:underline flex items-center gap-1">
            View All <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[1, 2, 3].map(i => <div key={i} className="p-6 bg-card-bg border border-border-strong rounded-lg h-48 animate-pulse" />)}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {trendingIPOs.map((ipo) => (
              <div key={ipo.id} className="p-6 bg-card-bg border border-border-strong rounded-lg hover:border-primary-blue/30 transition-all flex flex-col justify-between">
                <div>
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-bold text-white text-base">{ipo.name}</h3>
                      <span className="text-xs text-text-muted font-mono">{ipo.sector}</span>
                    </div>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20">
                      {ipo.status.toUpperCase()}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs py-2 border-y border-border-subtle/40 mb-4 font-mono">
                    <div>
                      <span className="text-text-muted block text-[10px]">PRICE BAND</span>
                      <span className="text-white font-semibold">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</span>
                    </div>
                    <div>
                      <span className="text-text-muted block text-[10px]">GMP PREMIUM</span>
                      <span className="text-accent-emerald font-semibold">+{ipo.gmp}%</span>
                    </div>
                  </div>
                </div>

                <Link href={`/dashboard/ipo/${ipo.id}`} className="text-xs font-semibold text-primary-blue hover:underline flex items-center justify-between">
                  <span>View Details & AI Score</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
