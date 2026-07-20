'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Star, Trash2, Calendar, Sparkles } from 'lucide-react';
import { ipoService } from '../../../services/ipo.service';
import { IPO } from '../../../types';

export default function Watchlist() {
  const [items, setItems] = useState<IPO[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    ipoService.getIPOs(undefined, undefined, undefined, undefined, 1, 3)
      .then(res => {
        if (isMounted) {
          setItems(res.items);
          setLoading(false);
        }
      })
      .catch(err => {
        console.error('Failed to load watchlist items:', err);
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, []);

  const handleRemove = (id: string) => {
    setItems((prev) => prev.filter((i) => i.id !== id));
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex justify-between items-end border-b border-border-strong pb-3">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">My Watchlist</h1>
          <p className="text-xs text-text-muted">Monitor GMP premium trends and listing dates for saved deals.</p>
        </div>
        {items.length > 0 && (
          <button onClick={() => setItems([])} className="text-xs font-semibold text-red-400 hover:underline">
            Clear Watchlist
          </button>
        )}
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[1, 2, 3].map(i => <div key={i} className="p-6 bg-card-bg border border-border-strong rounded-lg h-96 animate-pulse" />)}
        </div>
      ) : items.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {items.map((ipo) => (
            <div key={ipo.id} className="p-6 rounded-lg bg-card-bg border border-border-strong flex flex-col justify-between h-96 relative">
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
                    <span className="text-[10px] text-text-muted font-mono">{ipo.sector}</span>
                  </div>
                </div>

                <div className="space-y-3.5 text-xs border-t border-border-subtle/30 pt-4 font-mono">
                  <div className="flex justify-between">
                    <span className="text-text-muted">GMP PREMIUM</span>
                    <span className="font-bold text-accent-emerald">+{ipo.gmp}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-muted">PRICE BAND</span>
                    <span className="text-white">₹{ipo.priceBand.min} - ₹{ipo.priceBand.max}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-muted">LOT SIZE</span>
                    <span className="text-white">{ipo.lotSize} Shares</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-text-muted">STATUS</span>
                    <span className="text-primary-blue font-bold">{ipo.status.toUpperCase()}</span>
                  </div>
                </div>
              </div>

              <Link
                href={`/dashboard/ipo/${ipo.id}`}
                className="w-full bg-dark-bg hover:bg-card-bg border border-border-subtle hover:border-primary-blue/40 text-text-primary text-xs font-semibold py-2.5 rounded-md flex items-center justify-center gap-1 transition-all mt-4"
              >
                View Detailed Analysis →
              </Link>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-16 text-center bg-card-bg border border-border-strong rounded-lg space-y-4">
          <Star className="w-12 h-12 text-text-muted mx-auto" />
          <h3 className="text-lg font-bold text-white">Your Watchlist is Empty</h3>
          <p className="text-xs text-text-muted max-w-sm mx-auto">
            Click the heart icon on any IPO deal card to bookmark it for real-time GMP alerts and listing updates.
          </p>
          <Link href="/dashboard/ipo" className="inline-block bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs px-6 py-3 rounded-md transition-all">
            Explore Active Deals
          </Link>
        </div>
      )}
    </div>
  );
}
