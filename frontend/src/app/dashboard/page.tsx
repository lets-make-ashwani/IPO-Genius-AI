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
  Clock,
  Award,
  DollarSign,
  Users
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { ipoService } from '../../services/ipo.service';
import { IPO } from '../../types';

type CategoryType = 'live' | 'upcoming' | 'recently-listed' | 'recently-closed' | 'top-rated' | 'highest-gmp' | 'most-subscribed' | 'trending';

export default function DashboardHome() {
  const { user } = useAuth();
  const [counts, setCounts] = useState({ total: 0, open: 0, upcoming: 0, listed: 0 });
  const [countsLoading, setCountsLoading] = useState(true);
  
  // Interactive Tabbed Catalog
  const [activeTab, setActiveTab] = useState<CategoryType>('live');
  const [tabItems, setTabItems] = useState<IPO[]>([]);
  const [tabLoading, setTabLoading] = useState(true);
  const [lastSynced, setLastSynced] = useState<string>('');

  // Tabs Configuration
  const tabs = [
    { id: 'live', label: 'Live IPOs', icon: Circle, color: 'text-accent-emerald' },
    { id: 'upcoming', label: 'Upcoming', icon: Calendar, color: 'text-primary-blue' },
    { id: 'recently-listed', label: 'Recently Listed', icon: TrendingUp, color: 'text-accent-emerald' },
    { id: 'recently-closed', label: 'Recently Closed', icon: Clock, color: 'text-text-muted' },
    { id: 'top-rated', label: 'Top AI Rated', icon: Award, color: 'text-secondary-purple' },
    { id: 'highest-gmp', label: 'Highest GMP', icon: DollarSign, color: 'text-accent-emerald' },
    { id: 'most-subscribed', label: 'Most Subscribed', icon: Users, color: 'text-primary-blue' },
    { id: 'trending', label: 'Trending', icon: Sparkles, color: 'text-secondary-purple' }
  ];

  // Fetch counts once on load
  useEffect(() => {
    Promise.all([
      ipoService.getIPOs(undefined, undefined, undefined, undefined, 1, 1),
      ipoService.getIPOs(undefined, 'OPEN', undefined, undefined, 1, 1),
      ipoService.getIPOs(undefined, 'UPCOMING', undefined, undefined, 1, 1),
      ipoService.getIPOs(undefined, 'LISTED', undefined, undefined, 1, 1),
    ]).then(([allRes, openRes, upcomingRes, listedRes]) => {
      setCounts({
        total: allRes.total || 0,
        open: openRes.total || 0,
        upcoming: upcomingRes.total || 0,
        listed: listedRes.total || 0
      });
      setCountsLoading(false);
    }).catch(err => {
      console.error('Failed to load counts:', err);
      setCountsLoading(false);
    });
  }, []);

  // Fetch tab items on tab/date change
  useEffect(() => {
    setTabLoading(true);
    ipoService.getIPOsByCategory(activeTab, 1, 3)
      .then(res => {
        setTabItems(res.items);
        setTabLoading(false);
        const now = new Date();
        const istTime = now.toLocaleTimeString('en-US', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', second: '2-digit' });
        setLastSynced(`${istTime} IST`);
      })
      .catch(err => {
        console.error(`Failed to load category ${activeTab}:`, err);
        setTabLoading(false);
      });
  }, [activeTab]);

  const userName = user?.name ? user.name.split(' ')[0] : 'Investor';

  return (
    <div className="space-y-6 sm:space-y-8 max-w-full overflow-x-hidden">
      {/* Greeting & Date Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-white mb-1">Good day, {userName} 👋</h1>
          <p className="text-xs text-text-muted">Here is your live IPO market intelligence recap.</p>
        </div>
        <span className="text-[11px] sm:text-xs font-semibold text-text-muted font-mono bg-card-bg border border-border-strong px-3 py-1.5 rounded-md self-start sm:self-auto">
          {new Date().toLocaleDateString('en-IN', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' })}
        </span>
      </div>

      {/* Responsive KPI Grid */}
      <div className="grid grid-cols-1 min-[480px]:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        {[
          { label: 'Total IPOs Tracked', val: counts.total, desc: 'Live persisted deals', icon: BarChart3, iconColor: 'text-primary-blue bg-primary-blue/10' },
          { label: 'Currently Open', val: counts.open, desc: 'Bidding active now', icon: Circle, iconColor: 'text-accent-emerald bg-accent-emerald/10' },
          { label: 'Upcoming Issues', val: counts.upcoming, desc: 'Filing pipeline', icon: Calendar, iconColor: 'text-secondary-purple bg-secondary-purple/10' },
          { label: 'Recently Listed', val: counts.listed, desc: 'Exchange traded', icon: TrendingUp, iconColor: 'text-accent-emerald bg-accent-emerald/10' }
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="p-4 sm:p-5 md:p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col justify-between hover:border-border-subtle transition-all">
              <div className="flex justify-between items-start">
                <div className="min-w-0 flex-1">
                  <span className="text-[10px] sm:text-xs font-bold text-text-muted block mb-1 uppercase tracking-wider truncate">{card.label}</span>
                  <span className="text-2xl sm:text-3xl font-extrabold text-white font-mono">{countsLoading ? '...' : card.val}</span>
                </div>
                <div className={`p-2 sm:p-2.5 rounded-md shrink-0 ${card.iconColor}`}>
                  <Icon className="w-4 h-4 sm:w-5 sm:h-5" />
                </div>
              </div>
              <span className="text-[10px] sm:text-[11px] text-text-muted mt-3 sm:mt-4 block">{card.desc}</span>
            </div>
          );
        })}
      </div>

      {/* Interactive Tabbed Market Sections */}
      <div className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <h2 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-4 h-4 sm:w-5 sm:h-5 text-secondary-purple shrink-0" /> Market Catalogs
          </h2>
          <span className="text-[10px] sm:text-xs text-text-muted bg-sidebar-bg/60 border border-border-strong px-2.5 py-1 rounded-sm font-mono self-start sm:self-auto">
            Sync active: {lastSynced || 'syncing...'}
          </span>
        </div>

        {/* Tab Controls */}
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-thin">
          {tabs.map((tab) => {
            const TabIcon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as CategoryType)}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-md border text-xs font-semibold whitespace-nowrap transition-all ${
                  isActive 
                    ? 'bg-primary-blue border-primary-blue text-white shadow-lg shadow-primary-blue/15' 
                    : 'bg-card-bg border-border-strong text-text-muted hover:text-white hover:border-border-subtle'
                }`}
              >
                <TabIcon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : tab.color}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Tab Content Preview */}
        {tabLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
            {[1, 2, 3].map(i => <div key={i} className="p-6 bg-card-bg border border-border-strong rounded-lg h-44 animate-pulse" />)}
          </div>
        ) : tabItems.length > 0 ? (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
              {tabItems.map((ipo) => (
                <div key={ipo.id} className="p-4 sm:p-6 bg-card-bg border border-border-strong rounded-lg hover:border-primary-blue/30 transition-all flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex justify-between items-start gap-2 mb-3">
                      <div className="min-w-0 flex-1">
                        <h3 className="font-bold text-white text-sm sm:text-base truncate">{ipo.name}</h3>
                        <span className="text-xs text-text-muted font-mono block truncate">{ipo.sector}</span>
                      </div>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full shrink-0 ${
                        ipo.computedStatus === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                        ipo.computedStatus === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20' :
                        'bg-dark-bg text-text-muted border border-border-subtle'
                      }`}>
                        {ipo.computedStatus?.toUpperCase()}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-xs py-2 border-y border-border-subtle/40 font-mono">
                      <div>
                        <span className="text-text-muted block text-[10px]">PRICE BAND</span>
                        <span className="text-white font-semibold truncate block">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</span>
                      </div>
                      <div>
                        <span className="text-text-muted block text-[10px]">GMP PREMIUM</span>
                        <span className={`font-semibold truncate block ${ipo.gmp > 0 ? 'text-accent-emerald' : 'text-text-muted'}`}>
                          {ipo.gmp > 0 ? `+${ipo.gmp}%` : '0%'}
                        </span>
                      </div>
                      <div>
                        <span className="text-text-muted block text-[10px]">SUBSCRIPTION</span>
                        <span className="text-white font-semibold truncate block">
                          {ipo.totalSubscription && ipo.totalSubscription > 0 ? `${ipo.totalSubscription}x` : 'N/A'}
                        </span>
                      </div>
                      <div>
                        <span className="text-text-muted block text-[10px]">TIMELINE</span>
                        <span className="text-text-secondary truncate block">{ipo.openDate}</span>
                      </div>
                    </div>
                  </div>

                  <Link href={`/dashboard/ipo/${ipo.id}`} className="text-xs font-semibold text-primary-blue hover:underline flex items-center justify-between min-h-[44px]">
                    <span>Analyze Deal & SWOT</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              ))}
            </div>

            {/* View All Link */}
            <div className="flex justify-end pt-2">
              <Link 
                href={`/ipos/${activeTab}`} 
                className="text-xs font-bold text-primary-blue hover:underline inline-flex items-center gap-1.5 min-h-[44px]"
              >
                View all in {tabs.find(t => t.id === activeTab)?.label} <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        ) : (
          <div className="py-12 text-center bg-card-bg border border-border-strong rounded-lg">
            <span className="text-xs text-text-muted">No IPOs currently found in this category.</span>
          </div>
        )}
      </div>
    </div>
  );
}
