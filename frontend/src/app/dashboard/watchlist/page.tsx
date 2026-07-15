'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Star, Trash2, Calendar, Sparkles } from 'lucide-react';
import { mockIPOs } from '../../../constants/mockData';
import { IPO } from '../../../types';

export default function Watchlist() {
  const [items, setItems] = useState<IPO[]>(mockIPOs.slice(0, 3));

  const handleRemove = (id: string) => {
    setItems((prev) => prev.filter((i) => i.id !== id));
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex justify-between items-end border-b border-border-strong pb-3">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">My Watchlist</h1>
          <p className="text-xs text-text-muted">Monitor GMP premium trends and allotment dates.</p>
        </div>
        {items.length > 0 && (
          <button onClick={() => setItems([])} className="text-xs font-semibold text-red-400 hover:underline">
            Clear All
          </button>
        )}
      </div>

      {items.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {items.map((ipo) => (
            <div key={ipo.id} className="p-6 rounded-lg bg-card-bg border border-border-strong flex flex-col justify-between h-96 relative">
              {/* Remove button absolute */}
              <button
                onClick={() => handleRemove(ipo.id)}
                className="absolute top-6 right-6 p-2 rounded-md hover:bg-red-500/10 text-text-muted hover:text-red-400 transition-colors"
                title="Remove from watchlist"
              >
                <Trash2 className="w-4 h-4" />
              </button>

              <div>
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-md bg-gradient-to-br from-primary-blue/10 to-secondary-purple/10 flex items-center justify-center font-bold text-primary-blue font-mono">
                    {ipo.ticker.substring(0, 2)}
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-white leading-tight">{ipo.name}</h3>
                    <span className="text-[10px] text-text-muted font-mono">{ipo.ticker}</span>
                  </div>
                </div>

                <div className="space-y-3.5 text-xs border-t border-border-subtle/30 pt-4">
                  <div className="flex justify-between">
                    <span className="text-text-muted">GMP PREMIUM</span>
                    <span className="font-bold text-accent-emerald font-mono">+{ipo.gmp}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-muted">PRICE BAND</span>
                    <span className="font-bold text-white font-mono">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-muted">LISTING DATE</span>
                    <span className="font-bold text-white font-mono">{new Date(ipo.listingDate).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between border-t border-border-subtle/30 pt-4 mt-6">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full border-2 border-accent-emerald flex items-center justify-center font-bold text-xs text-accent-emerald font-mono">
                    {ipo.aiScore}
                  </div>
                  <div className="text-left leading-none">
                    <span className="text-[9px] text-text-muted block">AI SCORE</span>
                    <span className="text-[10px] font-bold text-white">{ipo.aiRecommendation}</span>
                  </div>
                </div>
                <Link href={`/dashboard/ipo/${ipo.id}`} className="text-xs font-semibold bg-border-subtle hover:bg-border-strong text-white px-3 py-1.5 rounded-md transition-colors">
                  Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* Empty Watchlist State */
        <div className="flex flex-col items-center justify-center py-24 text-center space-y-4 bg-card-bg/25 border border-border-strong border-dashed rounded-lg">
          <div className="p-4 rounded-full bg-border-strong text-text-muted">
            <Star className="w-10 h-10" />
          </div>
          <div className="space-y-1">
            <h3 className="text-white font-bold text-base">Your watchlist is empty</h3>
            <p className="text-xs text-text-secondary max-w-sm">Save upcoming or open IPO listings to track their premiums and alerts in one dashboard.</p>
          </div>
          <Link href="/dashboard/ipo" className="bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs px-5 py-2.5 rounded-md shadow-md transition-all">
            Browse All IPOs
          </Link>
        </div>
      )}
    </div>
  );
}
