'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { 
  Sparkles, 
  ArrowLeft, 
  TrendingUp, 
  Star, 
  Calendar, 
  DollarSign, 
  Clock, 
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { ipoService } from '../services/ipo.service';
import { IPO } from '../types';
import Navbar from './Navbar';
import Footer from './Footer';

interface IPOListPageProps {
  category: string;
  title: string;
  description: string;
}

export default function IPOListPage({ category, title, description }: IPOListPageProps) {
  const [ipos, setIpos] = useState<IPO[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [lastUpdated, setLastUpdated] = useState<string>('');
  const limit = 10;

  useEffect(() => {
    setLoading(true);
    ipoService.getIPOsByCategory(category, page, limit)
      .then(res => {
        setIpos(res.items);
        setTotal(res.total);
        setLoading(false);
        // Set last updated timestamp in IST
        const now = new Date();
        const istTime = now.toLocaleTimeString('en-US', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', second: '2-digit' });
        setLastUpdated(`${istTime} IST`);
      })
      .catch(err => {
        console.error('Failed to load categorized IPOs:', err);
        setLoading(false);
      });
  }, [category, page]);

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col pt-16">
      <Navbar />

      <main className="flex-1 max-w-6xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-12">
        {/* Back Link */}
        <Link href="/" className="inline-flex items-center gap-2 text-sm text-text-muted hover:text-white transition-colors mb-8">
          <ArrowLeft className="w-4 h-4" /> Back to Home
        </Link>

        {/* Header Block */}
        <div className="flex flex-col md:flex-row md:items-end justify-between border-b border-border-strong/50 pb-8 mb-10 gap-6">
          <div>
            <div className="flex items-center gap-2 bg-gradient-to-r from-primary-blue/10 to-secondary-purple/10 border border-secondary-purple/20 px-3 py-1 rounded-full text-xs font-semibold text-secondary-purple w-fit mb-3">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Real-Time Indexing</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">{title}</h1>
            <p className="text-text-secondary mt-2 text-sm sm:text-base max-w-2xl">{description}</p>
          </div>

          {/* Telemetry/Freshness Badge */}
          <div className="flex flex-col items-start md:items-end bg-sidebar-bg/40 border border-border-subtle p-4 rounded-lg min-w-[200px]">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-accent-emerald animate-pulse" />
              <span className="text-xs font-bold text-accent-emerald uppercase tracking-wider">Sync Active</span>
            </div>
            <span className="text-xs text-text-muted mt-1.5 font-mono">Last updated: {lastUpdated || 'Updating...'}</span>
          </div>
        </div>

        {/* Content Section */}
        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-32 bg-card-bg border border-border-strong animate-pulse rounded-lg" />
            ))}
          </div>
        ) : ipos.length > 0 ? (
          <div className="space-y-6">
            {/* Desktop Table View */}
            <div className="hidden md:block overflow-hidden bg-card-bg border border-border-strong rounded-lg shadow-xl">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-border-strong bg-sidebar-bg/60 text-xs font-bold uppercase tracking-wider text-text-muted">
                    <th className="p-4">Company Name</th>
                    <th className="p-4">Dynamic Status</th>
                    <th className="p-4">Price Band</th>
                    <th className="p-4">GMP Premium</th>
                    <th className="p-4">Subscription</th>
                    <th className="p-4">Timeline</th>
                    <th className="p-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle/30 text-sm">
                  {ipos.map(ipo => (
                    <tr key={ipo.id} className="hover:bg-sidebar-bg/25 transition-colors group">
                      <td className="p-4">
                        <div>
                          <div className="font-bold text-white group-hover:text-primary-blue transition-colors">{ipo.name}</div>
                          <span className="text-xs text-text-muted font-mono">{ipo.sector}</span>
                        </div>
                      </td>
                      <td className="p-4">
                        <div className="flex flex-col gap-1">
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full w-fit ${
                            ipo.computedStatus === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                            ipo.computedStatus === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20' :
                            'bg-dark-bg text-text-muted border border-border-subtle'
                          }`}>
                            {ipo.computedStatus?.toUpperCase()}
                          </span>
                          {/* Alert Badges */}
                          {ipo.listingToday && (
                            <span className="text-[10px] font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2 py-0.5 rounded-sm w-fit">
                              LISTING TODAY
                            </span>
                          )}
                          {ipo.openingToday && (
                            <span className="text-[10px] font-semibold bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20 px-2 py-0.5 rounded-sm w-fit">
                              OPENING TODAY
                            </span>
                          )}
                          {ipo.openingTomorrow && (
                            <span className="text-[10px] font-semibold bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 px-2 py-0.5 rounded-sm w-fit">
                              OPENING TOMORROW
                            </span>
                          )}
                          {ipo.closingToday && (
                            <span className="text-[10px] font-semibold bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-0.5 rounded-sm w-fit animate-pulse">
                              CLOSING TODAY
                            </span>
                          )}
                          {ipo.closingTomorrow && (
                            <span className="text-[10px] font-semibold bg-orange-500/10 text-orange-400 border border-orange-500/20 px-2 py-0.5 rounded-sm w-fit">
                              CLOSING TOMORROW
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="p-4 font-mono font-semibold text-white">
                        ₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}
                      </td>
                      <td className="p-4">
                        <span className={`font-semibold ${ipo.gmp > 0 ? 'text-accent-emerald' : 'text-text-muted'}`}>
                          {ipo.gmp > 0 ? `+${ipo.gmp}%` : '0%'}
                        </span>
                      </td>
                      <td className="p-4 font-semibold text-white">
                        {ipo.totalSubscription && ipo.totalSubscription > 0 ? `${ipo.totalSubscription}x` : 'N/A'}
                      </td>
                      <td className="p-4 text-xs font-mono text-text-secondary space-y-0.5">
                        <div>Open: {ipo.openDate}</div>
                        <div>Close: {ipo.closeDate}</div>
                        {ipo.listingDate && ipo.listingDate !== 'TBD' && (
                          <div className="text-primary-blue">List: {ipo.listingDate}</div>
                        )}
                      </td>
                      <td className="p-4 text-right">
                        <Link 
                          href={`/dashboard/ipo/${ipo.id}`} 
                          className="bg-dark-bg hover:bg-primary-blue text-text-primary hover:text-white px-4 py-2 rounded border border-border-subtle hover:border-primary-blue text-xs font-semibold transition-all inline-block"
                        >
                          Analyze
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Mobile Stacked Deal Cards */}
            <div className="md:hidden space-y-4">
              {ipos.map(ipo => (
                <div key={ipo.id} className="p-5 bg-card-bg border border-border-strong rounded-lg flex flex-col gap-4 relative">
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-extrabold text-white text-base leading-tight">{ipo.name}</h4>
                      <span className="text-xs text-text-muted font-mono">{ipo.sector}</span>
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      ipo.computedStatus === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                      ipo.computedStatus === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20' :
                      'bg-dark-bg text-text-muted border border-border-subtle'
                    }`}>
                      {ipo.computedStatus?.toUpperCase()}
                    </span>
                  </div>

                  {/* Mobile Alerts */}
                  <div className="flex flex-wrap gap-1.5">
                    {ipo.listingToday && (
                      <span className="text-[9px] font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2 py-0.5 rounded-sm">
                        LISTING TODAY
                      </span>
                    )}
                    {ipo.openingToday && (
                      <span className="text-[9px] font-bold bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20 px-2 py-0.5 rounded-sm">
                        OPENING TODAY
                      </span>
                    )}
                    {ipo.openingTomorrow && (
                      <span className="text-[9px] font-bold bg-yellow-500/10 text-yellow-400 border border-yellow-500/20 px-2 py-0.5 rounded-sm">
                        OPENING TOMORROW
                      </span>
                    )}
                    {ipo.closingToday && (
                      <span className="text-[9px] font-bold bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-0.5 rounded-sm animate-pulse">
                        CLOSING TODAY
                      </span>
                    )}
                    {ipo.closingTomorrow && (
                      <span className="text-[9px] font-bold bg-orange-500/10 text-orange-400 border border-orange-500/20 px-2 py-0.5 rounded-sm">
                        CLOSING TOMORROW
                      </span>
                    )}
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-xs font-mono border-t border-b border-border-subtle/40 py-3">
                    <div>
                      <span className="text-text-muted block text-[10px] mb-0.5">PRICE BAND</span>
                      <span className="font-bold text-white">₹{ipo.priceBand.min} - {ipo.priceBand.max}</span>
                    </div>
                    <div>
                      <span className="text-text-muted block text-[10px] mb-0.5">GMP PREMIUM</span>
                      <span className={`font-bold ${ipo.gmp > 0 ? 'text-accent-emerald' : 'text-text-muted'}`}>
                        {ipo.gmp > 0 ? `+${ipo.gmp}%` : '0%'}
                      </span>
                    </div>
                    <div>
                      <span className="text-text-muted block text-[10px] mb-0.5">SUBSCRIPTION</span>
                      <span className="font-bold text-white">{ipo.totalSubscription ? `${ipo.totalSubscription}x` : 'N/A'}</span>
                    </div>
                    <div>
                      <span className="text-text-muted block text-[10px] mb-0.5">TIMELINE</span>
                      <span className="font-bold text-text-secondary">Open: {ipo.openDate}</span>
                    </div>
                  </div>

                  <Link 
                    href={`/dashboard/ipo/${ipo.id}`} 
                    className="w-full bg-dark-bg hover:bg-card-bg border border-border-subtle hover:border-primary-blue text-text-primary text-xs font-semibold py-3 rounded-md flex items-center justify-center gap-1 transition-all"
                  >
                    Analyze Deal
                  </Link>
                </div>
              ))}
            </div>

            {/* Pagination Controls */}
            {total > limit && (
              <div className="flex justify-between items-center border-t border-border-strong/40 pt-6">
                <button
                  disabled={page === 1}
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                  className="px-4 py-2 border border-border-subtle rounded text-xs font-semibold hover:bg-card-bg disabled:opacity-50 disabled:pointer-events-none transition-colors"
                >
                  Previous
                </button>
                <span className="text-xs text-text-muted">
                  Page {page} of {Math.ceil(total / limit)}
                </span>
                <button
                  disabled={page * limit >= total}
                  onClick={() => setPage(p => p + 1)}
                  className="px-4 py-2 border border-border-subtle rounded text-xs font-semibold hover:bg-card-bg disabled:opacity-50 disabled:pointer-events-none transition-colors"
                >
                  Next
                </button>
              </div>
            )}
          </div>
        ) : (
          <div className="py-24 text-center bg-card-bg border border-border-strong rounded-lg">
            <AlertCircle className="w-12 h-12 text-text-muted mx-auto mb-4" />
            <h3 className="text-lg font-bold text-white mb-1">No IPOs found</h3>
            <p className="text-xs text-text-muted">There are currently no IPOs listed in this category.</p>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
