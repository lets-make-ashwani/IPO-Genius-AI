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
    <div className="space-y-6">
      {/* Title */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">IPO Listings</h1>
          <p className="text-xs text-text-muted">Browse active, upcoming, and listed market opportunities.</p>
        </div>
        <span className="text-xs font-mono bg-card-bg border border-border-strong px-3 py-1 rounded text-text-secondary">
          Live FastAPI Backend
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
            className="w-full h-10 pl-10 pr-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all"
          />
        </div>

        {/* Right options */}
        <div className="flex flex-wrap items-center gap-4 w-full md:w-auto">
          {/* Status filter */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-text-muted font-bold uppercase tracking-wider">Status:</span>
            <select
              value={selectedStatus}
              onChange={(e) => {
                setSelectedStatus(e.target.value);
                setPage(1);
              }}
              className="h-9 px-3 rounded bg-dark-bg border border-border-subtle text-xs text-text-secondary focus:outline-none focus:border-primary-blue"
            >
              {statuses.map(st => <option key={st}>{st}</option>)}
            </select>
          </div>

          {/* Sector filter */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-text-muted font-bold uppercase tracking-wider">Sector:</span>
            <select
              value={selectedSector}
              onChange={(e) => {
                setSelectedSector(e.target.value);
                setPage(1);
              }}
              className="h-9 px-3 rounded bg-dark-bg border border-border-subtle text-xs text-text-secondary focus:outline-none focus:border-primary-blue"
            >
              {sectors.map(sec => <option key={sec}>{sec}</option>)}
            </select>
          </div>

          {/* View toggle */}
          <div className="flex items-center border border-border-subtle rounded overflow-hidden">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 transition-colors ${viewMode === 'grid' ? 'bg-primary-blue text-white' : 'bg-dark-bg text-text-muted hover:text-white'}`}
              title="Grid View"
            >
              <Grid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-2 transition-colors ${viewMode === 'table' ? 'bg-primary-blue text-white' : 'bg-dark-bg text-text-muted hover:text-white'}`}
              title="Table View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Loading Skeletons */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[1, 2, 3, 4, 5, 6].map((idx) => (
            <div key={idx} className="p-6 rounded-lg bg-card-bg border border-border-strong animate-pulse h-96 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex justify-between">
                  <div className="w-10 h-10 bg-border-subtle rounded-md" />
                  <div className="w-16 h-6 bg-border-subtle rounded-full" />
                </div>
                <div className="h-6 w-3/4 bg-border-subtle rounded" />
                <div className="h-4 w-1/2 bg-border-subtle rounded" />
                <div className="h-20 bg-border-subtle rounded" />
              </div>
              <div className="h-10 bg-border-subtle rounded" />
            </div>
          ))}
        </div>
      ) : viewMode === 'grid' ? (
        /* Grid Mode View */
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {ipos.length > 0 ? (
            ipos.map((ipo) => (
              <div key={ipo.id} className="p-6 rounded-lg bg-card-bg border border-border-strong hover:border-primary-blue/30 transition-all flex flex-col justify-between h-96">
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <div className="w-10 h-10 rounded-md bg-gradient-to-br from-primary-blue/10 to-secondary-purple/10 flex items-center justify-center font-bold text-primary-blue font-mono">
                      {ipo.ticker.substring(0, 2)}
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                      ipo.status === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue border border-primary-blue/20' :
                      'bg-dark-bg text-text-muted border border-border-subtle'
                    }`}>
                      {ipo.status.toUpperCase()}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-white mb-1 line-clamp-1">{ipo.name}</h3>
                  <span className="text-xs text-text-muted mb-4 block font-mono">Sector: {ipo.sector}</span>

                  <div className="grid grid-cols-2 gap-4 py-3 border-y border-border-subtle/50 text-xs mb-4">
                    <div>
                      <span className="text-[10px] text-text-muted block font-mono">PRICE BAND</span>
                      <span className="font-semibold text-white">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-text-muted block font-mono">LOT SIZE</span>
                      <span className="font-semibold text-white">{ipo.lotSize} Shares</span>
                    </div>
                  </div>

                  <div className="space-y-1 text-xs mb-4">
                    <div className="flex justify-between">
                      <span className="text-text-muted">Issue Open:</span>
                      <span className="font-semibold text-text-secondary">{ipo.openDate}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-text-muted">Issue Close:</span>
                      <span className="font-semibold text-text-secondary">{ipo.closeDate}</span>
                    </div>
                  </div>
                </div>

                <Link
                  href={`/dashboard/ipo/${ipo.id}`}
                  className="w-full bg-dark-bg hover:bg-card-bg border border-border-subtle hover:border-primary-blue/40 text-text-primary text-xs font-semibold py-2.5 rounded-md flex items-center justify-center gap-1 transition-all"
                >
                  View Details & AI Score <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))
          ) : (
            <div className="col-span-3 py-16 text-center bg-card-bg border border-border-strong rounded-lg">
              <Filter className="w-10 h-10 text-text-muted mx-auto mb-3" />
              <h3 className="text-base font-bold text-white mb-1">No IPOs Found</h3>
              <p className="text-xs text-text-muted">Try clearing search terms or selecting another sector/status filter.</p>
            </div>
          )}
        </div>
      ) : (
        /* Table Mode View */
        <div className="bg-card-bg border border-border-strong rounded-lg overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-dark-bg/60 text-text-muted uppercase text-[10px] font-mono border-b border-border-subtle">
              <tr>
                <th className="p-4">Company Name</th>
                <th className="p-4">Status</th>
                <th className="p-4">Price Band</th>
                <th className="p-4">Lot Size</th>
                <th className="p-4">Open Date</th>
                <th className="p-4">Close Date</th>
                <th className="p-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle/50 text-text-secondary">
              {ipos.map((ipo) => (
                <tr key={ipo.id} className="hover:bg-dark-bg/40 transition-colors">
                  <td className="p-4 font-semibold text-white">
                    {ipo.name}
                    <span className="block text-[10px] text-text-muted font-mono">{ipo.sector}</span>
                  </td>
                  <td className="p-4">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20' :
                      'bg-primary-blue/10 text-primary-blue border border-primary-blue/20'
                    }`}>
                      {ipo.status}
                    </span>
                  </td>
                  <td className="p-4 font-mono">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</td>
                  <td className="p-4 font-mono">{ipo.lotSize}</td>
                  <td className="p-4">{ipo.openDate}</td>
                  <td className="p-4">{ipo.closeDate}</td>
                  <td className="p-4 text-right">
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

      {/* Pagination Controls */}
      {!loading && total > limit && (
        <div className="flex items-center justify-between pt-4 border-t border-border-subtle">
          <span className="text-xs text-text-muted">
            Showing Page {page} of {totalPages} ({total} total IPOs)
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 bg-card-bg border border-border-subtle rounded text-text-muted hover:text-white disabled:opacity-40"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
              className="p-2 bg-card-bg border border-border-subtle rounded text-text-muted hover:text-white disabled:opacity-40"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
