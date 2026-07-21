'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Search, Grid, List, Sparkles, Filter, ChevronRight, ChevronLeft, RefreshCw } from 'lucide-react';
import { ipoService } from '../../../services/ipo.service';
import { IPO } from '../../../types';

export default function IPOListing() {
  const [search, setSearch] = useState('');
  const [selectedSector, setSelectedSector] = useState('All');
  const [selectedStatus, setSelectedStatus] = useState('All');
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [ipos, setIpos] = useState<IPO[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const limit = 9;

  const sectors = ['All', 'FMCG', 'EV', 'Finance', 'Technology', 'Healthcare', 'Automobile'];
  const statuses = ['All', 'Open', 'Upcoming', 'Closed', 'Listed'];

  useEffect(() => {
    let isMounted = true;
    setLoading(true);

    ipoService.getIPOs(search, selectedStatus, selectedSector, 'All', page, limit)
      .then((res) => {
        if (isMounted) {
          setIpos(res.items);
          setTotal(res.total);
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error('Failed to load IPOs:', err);
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [search, selectedStatus, selectedSector, page]);

  const totalPages = Math.ceil(total / limit) || 1;

  return (
    <div className="space-y-6 max-w-full overflow-x-hidden">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-white mb-1">IPO Listings</h1>
          <p className="text-xs text-text-muted">Browse active, upcoming, and listed market opportunities.</p>
        </div>
        <span className="text-[11px] sm:text-xs font-mono bg-card-bg border border-border-strong px-3 py-1 rounded text-text-secondary self-start sm:self-auto">
          {total} Total Deals
        </span>
      </div>

      {/* Filters Control Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-card-bg border border-border-strong p-4 rounded-lg">
        {/* Left search */}
        <div className="relative w-full md:w-80">
          <Search className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
          <input
            type="text"
            placeholder="Search by company or sector..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            className="w-full h-10 pl-10 pr-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all text-white placeholder:text-text-muted"
          />
        </div>

        {/* Right options */}
        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          {/* Status filter */}
          <div className="flex items-center gap-2 w-full sm:w-auto">
            <span className="text-xs text-text-muted font-bold uppercase tracking-wider shrink-0">Status:</span>
            <select
              value={selectedStatus}
              onChange={(e) => {
                setSelectedStatus(e.target.value);
                setPage(1);
              }}
              className="h-10 px-3 rounded bg-dark-bg border border-border-subtle text-xs text-text-secondary focus:outline-none focus:border-primary-blue flex-1 sm:flex-initial"
            >
              {statuses.map(st => <option key={st}>{st}</option>)}
            </select>
          </div>

          {/* Sector filter */}
          <div className="flex items-center gap-2 w-full sm:w-auto">
            <span className="text-xs text-text-muted font-bold uppercase tracking-wider shrink-0">Sector:</span>
            <select
              value={selectedSector}
              onChange={(e) => {
                setSelectedSector(e.target.value);
                setPage(1);
              }}
              className="h-10 px-3 rounded bg-dark-bg border border-border-subtle text-xs text-text-secondary focus:outline-none focus:border-primary-blue flex-1 sm:flex-initial"
            >
              {sectors.map(sec => <option key={sec}>{sec}</option>)}
            </select>
          </div>

          {/* View toggle (desktop/tablet) */}
          <div className="hidden sm:flex items-center bg-dark-bg border border-border-subtle rounded p-1 gap-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded text-xs transition-colors min-w-[36px] min-h-[36px] flex items-center justify-center ${viewMode === 'grid' ? 'bg-primary-blue text-white' : 'text-text-muted hover:text-white'}`}
              title="Grid View"
              aria-label="Grid View"
            >
              <Grid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-1.5 rounded text-xs transition-colors min-w-[36px] min-h-[36px] flex items-center justify-center ${viewMode === 'table' ? 'bg-primary-blue text-white' : 'text-text-muted hover:text-white'}`}
              title="Table View"
              aria-label="Table View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Content Rendering: Cards for Grid or Mobile / Table for Desktop */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="p-6 rounded-lg bg-card-bg border border-border-strong animate-pulse h-64" />
          ))}
        </div>
      ) : ipos.length > 0 ? (
        <>
          {/* Mobile Stacked Card View & Desktop Grid */}
          <div className={viewMode === 'grid' ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6' : 'grid grid-cols-1 md:hidden gap-4'}>
            {ipos.map((ipo) => (
              <div key={ipo.id} className="p-4 sm:p-6 rounded-lg bg-card-bg border border-border-strong hover:border-secondary-purple/20 transition-all flex flex-col justify-between space-y-4">
                <div>
                  <div className="flex items-start justify-between gap-3 mb-4">
                    <div className="min-w-0 flex-1">
                      <div className="w-10 h-10 rounded-md bg-gradient-to-br from-primary-blue/10 to-secondary-purple/10 flex items-center justify-center font-bold text-primary-blue mb-2 font-mono">
                        {ipo.name.charAt(0)}
                      </div>
                      <h3 className="text-base font-bold text-white leading-snug break-words">{ipo.name}</h3>
                      <span className="text-xs text-text-muted font-mono block truncate">{ipo.sector}</span>
                    </div>

                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full shrink-0 ${
                      ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                      ipo.status === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20' :
                      'bg-dark-bg text-text-muted border border-border-subtle'
                    }`}>
                      {ipo.status.toUpperCase()}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-3 mt-4 text-xs border-t border-border-subtle/40 pt-3 font-mono">
                    <div>
                      <span className="text-text-muted block text-[10px] mb-0.5">PRICE BAND</span>
                      <span className="font-bold text-white block truncate">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</span>
                    </div>
                    <div>
                      <span className="text-text-muted block text-[10px] mb-0.5">GMP PREMIUM</span>
                      <span className="font-bold text-accent-emerald block truncate">+{ipo.gmp}%</span>
                    </div>
                  </div>
                </div>

                <div className="pt-2 border-t border-border-subtle/30 flex items-center justify-between">
                  <div className="text-left">
                    <span className="text-[9px] text-text-muted block">AI RATING</span>
                    <span className="text-[10px] font-bold text-accent-emerald">{ipo.aiRecommendation || 'SUBSCRIBE'}</span>
                  </div>

                  <Link
                    href={`/dashboard/ipo/${ipo.id}`}
                    className="text-xs font-semibold text-primary-blue hover:underline flex items-center gap-1 min-h-[44px]"
                  >
                    View Details →
                  </Link>
                </div>
              </div>
            ))}
          </div>

          {/* Desktop Table View (hidden on mobile) */}
          {viewMode === 'table' && (
            <div className="hidden md:block bg-card-bg border border-border-strong rounded-lg overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-border-strong bg-dark-bg/60 text-text-muted uppercase text-[10px] font-mono">
                    <th className="p-4">Company Name</th>
                    <th className="p-4">Status</th>
                    <th className="p-4">Price Band</th>
                    <th className="p-4">Lot Size</th>
                    <th className="p-4">GMP</th>
                    <th className="p-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle/40 text-text-secondary font-mono">
                  {ipos.map((ipo) => (
                    <tr key={ipo.id} className="hover:bg-dark-bg/30 transition-colors">
                      <td className="p-4 font-semibold text-white font-sans">{ipo.name}</td>
                      <td className="p-4">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                          ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                          ipo.status === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20' :
                          'bg-dark-bg text-text-muted border border-border-subtle'
                        }`}>
                          {ipo.status.toUpperCase()}
                        </span>
                      </td>
                      <td className="p-4">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</td>
                      <td className="p-4">{ipo.lotSize}</td>
                      <td className="p-4 text-accent-emerald font-bold">+{ipo.gmp}%</td>
                      <td className="p-4 text-right font-sans">
                        <Link href={`/dashboard/ipo/${ipo.id}`} className="text-primary-blue hover:underline font-semibold">
                          Details →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      ) : (
        <div className="p-12 text-center bg-card-bg border border-border-strong rounded-lg">
          <p className="text-sm text-text-muted">No IPOs found matching the selected filters.</p>
        </div>
      )}

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="flex justify-between items-center pt-4 border-t border-border-subtle">
          <button
            disabled={page === 1}
            onClick={() => setPage(prev => Math.max(1, prev - 1))}
            className="px-4 py-2 text-xs font-semibold bg-card-bg border border-border-strong rounded hover:bg-border-subtle disabled:opacity-50 text-white flex items-center gap-1 min-h-[44px]"
          >
            <ChevronLeft className="w-4 h-4" /> Previous
          </button>
          <span className="text-xs text-text-muted font-mono">
            Page {page} of {totalPages}
          </span>
          <button
            disabled={page === totalPages}
            onClick={() => setPage(prev => Math.min(totalPages, prev + 1))}
            className="px-4 py-2 text-xs font-semibold bg-card-bg border border-border-strong rounded hover:bg-border-subtle disabled:opacity-50 text-white flex items-center gap-1 min-h-[44px]"
          >
            Next <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}
