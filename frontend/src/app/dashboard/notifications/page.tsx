'use client';

import { useState } from 'react';
import { Bell, Sparkles, TrendingUp, Calendar, CreditCard, Trash2 } from 'lucide-react';

interface NotificationItem {
  id: string;
  type: 'alert' | 'gain' | 'ai' | 'billing';
  title: string;
  desc: string;
  time: string;
  read: boolean;
}

export default function Notifications() {
  const [filter, setFilter] = useState<'All' | 'Unread'>('All');
  
  const [items, setItems] = useState<NotificationItem[]>([
    { id: 'n1', type: 'alert', title: 'Swiggy IPO opens tomorrow — July 18, 2025', desc: 'Don\'t miss your chance to apply for Swiggy\'s IPO. Open from July 18-20.', time: '2 hours ago', read: false },
    { id: 'n2', type: 'gain', title: 'Bajaj Housing listed at +110% profit!', desc: 'Your watchlist IPO Bajaj Housing Finance made a strong debut on NSE/BSE, listing at 150 INR (issue price 70 INR).', time: '1 day ago', read: false },
    { id: 'n3', type: 'ai', title: 'AI Analysis updated for Ola Electric IPO', desc: 'New AI Score: 74/100. Growth potential indicators updated based on latest quarterly disclosures.', time: '2 days ago', read: false },
    { id: 'n4', type: 'billing', title: 'Your Pro subscription renews soon', desc: 'Your Pro Plan subscription will auto-renew on August 1, 2025 (499 INR). No actions needed.', time: '1 week ago', read: true },
    { id: 'n5', type: 'alert', title: 'Arkade Developers IPO Allotment is out', desc: 'Check your allotment status for Arkade Developers via Link Intime portal.', time: '1 week ago', read: true }
  ]);

  const handleMarkAllRead = () => {
    setItems((prev) => prev.map((item) => ({ ...item, read: true })));
  };

  const handleClearAll = () => {
    setItems([]);
  };

  const handleRemoveItem = (id: string) => {
    setItems((prev) => prev.filter((item) => item.id !== id));
  };

  const filteredItems = items.filter((item) => filter === 'All' || !item.read);

  const getIcon = (type: string) => {
    switch (type) {
      case 'alert': return <Bell className="w-4 h-4 text-primary-blue" />;
      case 'gain': return <TrendingUp className="w-4 h-4 text-accent-emerald" />;
      case 'ai': return <Sparkles className="w-4 h-4 text-secondary-purple" />;
      case 'billing': return <CreditCard className="w-4 h-4 text-yellow-500" />;
      default: return <Bell className="w-4 h-4 text-text-muted" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex justify-between items-end border-b border-border-strong pb-3">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">Notifications</h1>
          <p className="text-xs text-text-muted">Stay updated with IPO open/close events and AI evaluations.</p>
        </div>
        
        {items.length > 0 && (
          <div className="flex gap-4 text-xs font-semibold">
            <button onClick={handleMarkAllRead} className="text-primary-blue hover:underline">
              Mark all read
            </button>
            <button onClick={handleClearAll} className="text-red-400 hover:underline">
              Clear all
            </button>
          </div>
        )}
      </div>

      {/* Tabs */}
      <div className="flex border-b border-border-strong/60 gap-6 text-xs font-bold uppercase tracking-wider text-text-muted pb-3">
        <button
          onClick={() => setFilter('All')}
          className={`transition-colors ${filter === 'All' ? 'text-white border-b-2 border-primary-blue pb-3' : 'hover:text-white'}`}
        >
          All Notifications ({items.length})
        </button>
        <button
          onClick={() => setFilter('Unread')}
          className={`transition-colors ${filter === 'Unread' ? 'text-white border-b-2 border-primary-blue pb-3' : 'hover:text-white'}`}
        >
          Unread ({items.filter(i => !i.read).length})
        </button>
      </div>

      {/* List */}
      {filteredItems.length > 0 ? (
        <div className="space-y-4">
          {filteredItems.map((item) => (
            <div
              key={item.id}
              className={`p-4 rounded-lg bg-card-bg border flex gap-4 justify-between items-start transition-all ${
                item.read 
                  ? 'border-border-strong/50 opacity-80' 
                  : 'border-primary-blue/30 bg-blue-600/5 shadow-md border-l-4 border-l-primary-blue'
              }`}
            >
              <div className="flex gap-4 items-start">
                <div className={`p-2 rounded-md bg-dark-bg border border-border-subtle/40 mt-1`}>
                  {getIcon(item.type)}
                </div>
                <div>
                  <h4 className={`text-sm font-bold text-white mb-1 flex items-center gap-2`}>
                    {item.title}
                    {!item.read && <span className="w-1.5 h-1.5 rounded-full bg-primary-blue" />}
                  </h4>
                  <p className="text-xs text-text-secondary leading-relaxed mb-1">{item.desc}</p>
                  <span className="text-[10px] text-text-muted font-mono">{item.time}</span>
                </div>
              </div>

              <button
                onClick={() => handleRemoveItem(item.id)}
                className="p-1.5 rounded-md hover:bg-red-500/10 text-text-muted hover:text-red-400 transition-colors"
                title="Delete alert"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-20 text-text-muted text-xs bg-card-bg/25 border border-border-strong border-dashed rounded-lg">
          No notifications to display.
        </div>
      )}
    </div>
  );
}
