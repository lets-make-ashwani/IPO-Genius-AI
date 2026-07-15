'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Search, Grid, List, Sparkles, Filter, ChevronRight } from 'lucide-react';
import { mockIPOs } from '../../../constants/mockData';

export default function IPOListing() {
  const [search, setSearch] = useState('');
  const [selectedSector, setSelectedSector] = useState('All');
  const [selectedStatus, setSelectedStatus] = useState('All');
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');

  const sectors = ['All', 'FMCG', 'EV', 'Finance', 'Technology'];
  const statuses = ['All', 'Open', 'Upcoming', 'Closed', 'Listed'];

  const filteredIPOs = mockIPOs.filter((ipo) => {
    const matchesSearch = ipo.name.toLowerCase().includes(search.toLowerCase()) || ipo.ticker.toLowerCase().includes(search.toLowerCase());
    const matchesSector = selectedSector === 'All' || ipo.sector.includes(selectedSector);
    const matchesStatus = selectedStatus === 'All' || ipo.status.toLowerCase() === selectedStatus.toLowerCase();
    return matchesSearch && matchesSector && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">IPO Listings</h1>
        <p className="text-xs text-text-muted">Browse active, upcoming, and listed deals.</p>
      </div>

      {/* Filters Control Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-card-bg border border-border-strong p-4 rounded-lg">
        {/* Left search */}
        <div className="relative w-full md:w-80">
          <Search className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
          <input
            type="text"
            placeholder="Search by company or ticker..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
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
              onChange={(e) => setSelectedStatus(e.target.value)}
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
              onChange={(e) => setSelectedSector(e.target.value)}
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

      {/* Grid Mode View */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {filteredIPOs.length > 0 ? (
            filteredIPOs.map((ipo) => (
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
                  <span className="text-xs text-text-muted block mb-4">{ipo.sector}</span>
                  
                  <div className="grid grid-cols-2 gap-4 text-xs border-t border-border-subtle/40 pt-4">
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
                      <span className="text-[9px] text-text-muted block font-mono">AI SCORE</span>
                      <span className="text-[10px] font-bold text-white">{ipo.aiRecommendation}</span>
                    </div>
                  </div>
                  <Link href={`/dashboard/ipo/${ipo.id}`} className="text-xs font-semibold bg-border-subtle hover:bg-border-strong text-white px-3.5 py-2 rounded-md transition-colors">
                    Details →
                  </Link>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-full text-center py-20 text-text-muted bg-card-bg/30 rounded-lg border border-border-strong border-dashed">
              No IPOs match your search options.
            </div>
          )}
        </div>
      ) : (
        /* Table Mode View */
        <div className="bg-card-bg border border-border-strong rounded-lg overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-border-strong bg-dark-bg/40 text-xs font-bold text-text-muted uppercase tracking-wider">
                <th className="p-4 pl-6">Company</th>
                <th className="p-4">Sector</th>
                <th className="p-4">Price Band</th>
                <th className="p-4">Issue Size</th>
                <th className="p-4">Status</th>
                <th className="p-4">AI Score</th>
                <th className="p-4 pr-6 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="text-sm text-text-secondary divide-y divide-border-strong/30">
              {filteredIPOs.length > 0 ? (
                filteredIPOs.map((ipo) => (
                  <tr key={ipo.id} className="hover:bg-dark-bg/25 transition-colors">
                    <td className="p-4 pl-6 flex items-center gap-3">
                      <div className="w-8 h-8 rounded bg-primary-blue/10 flex items-center justify-center font-bold text-primary-blue text-sm font-mono">{ipo.ticker.substring(0, 2)}</div>
                      <div>
                        <span className="font-bold text-white block">{ipo.name}</span>
                        <span className="text-[10px] text-text-muted font-mono">{ipo.ticker}</span>
                      </div>
                    </td>
                    <td className="p-4 text-xs">{ipo.sector}</td>
                    <td className="p-4 font-mono font-semibold">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</td>
                    <td className="p-4 font-mono font-semibold">₹{ipo.issueSize} Cr</td>
                    <td className="p-4">
                      <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
                        ipo.status === 'Open' ? 'bg-accent-emerald/10 text-accent-emerald' :
                        ipo.status === 'Upcoming' ? 'bg-primary-blue/10 text-primary-blue' :
                        'bg-red-500/10 text-red-400'
                      }`}>
                        {ipo.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="p-4">
                      <span className={`text-xs font-bold font-mono px-2 py-0.5 rounded-full ${
                        ipo.aiScore >= 80 ? 'bg-accent-emerald/10 text-accent-emerald' : 'bg-yellow-500/10 text-yellow-500'
                      }`}>
                        {ipo.aiScore} ({ipo.aiRecommendation})
                      </span>
                    </td>
                    <td className="p-4 pr-6 text-right">
                      <Link href={`/dashboard/ipo/${ipo.id}`} className="text-xs font-semibold text-primary-blue hover:underline">
                        Details
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="text-center py-16 text-text-muted">
                    No IPOs match your search options.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
