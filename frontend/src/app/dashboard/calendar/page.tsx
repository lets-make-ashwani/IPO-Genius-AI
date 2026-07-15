'use client';

import { useState } from 'react';
import { ChevronLeft, ChevronRight, Calendar as CalendarIcon, Info } from 'lucide-react';

export default function Calendar() {
  const [currentDate, setCurrentDate] = useState(new Date(2026, 6, 16)); // Default to July 16, 2026
  const [selectedDay, setSelectedDay] = useState(18);

  const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  // July 2026 starts on a Wednesday (index 3)
  const daysInJuly = 31;
  const startDayIndex = 3;

  const calendarDays = [];
  for (let i = 0; i < startDayIndex; i++) {
    calendarDays.push(null);
  }
  for (let i = 1; i <= daysInJuly; i++) {
    calendarDays.push(i);
  }

  // July 2026 Mock IPO Events
  const events: Record<number, { title: string; type: 'open' | 'close' | 'listing' | 'allotment' }[]> = {
    8: [{ title: 'IndiGo IPO Opens', type: 'open' }],
    11: [{ title: 'IndiGo IPO Closes', type: 'close' }],
    12: [{ title: 'IndiGo Allotment', type: 'allotment' }],
    16: [
      { title: 'Swiggy IPO Opens', type: 'open' },
      { title: 'IndiGo Listing', type: 'listing' }
    ],
    18: [{ title: 'Swiggy IPO Closes', type: 'close' }],
    19: [{ title: 'Swiggy Allotment', type: 'allotment' }],
    21: [{ title: 'Ola Electric Opens', type: 'open' }],
    22: [{ title: 'Swiggy Listing', type: 'listing' }],
    24: [{ title: 'Ola Electric Closes', type: 'close' }]
  };

  const getEventBadgeColor = (type: string) => {
    switch (type) {
      case 'open': return 'bg-accent-emerald/20 text-accent-emerald border-accent-emerald/30';
      case 'close': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'allotment': return 'bg-secondary-purple/20 text-secondary-purple border-secondary-purple/30';
      case 'listing': return 'bg-primary-blue/20 text-primary-blue border-primary-blue/30';
      default: return 'bg-border-subtle/50 text-text-secondary';
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">IPO Calendar</h1>
          <p className="text-xs text-text-muted">Track bidding timelines, refunds, and listing days.</p>
        </div>
        
        <div className="flex items-center gap-4 bg-card-bg border border-border-strong px-4 py-2 rounded-md">
          <button className="p-1 rounded hover:bg-dark-bg text-text-muted hover:text-white transition-colors">
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="text-xs font-bold text-white font-mono">July 2026</span>
          <button className="p-1 rounded hover:bg-dark-bg text-text-muted hover:text-white transition-colors">
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-4 text-[10px] font-semibold text-text-secondary">
        <div className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-accent-emerald" /> Bidding Opens</div>
        <div className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-red-500" /> Bidding Closes</div>
        <div className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-secondary-purple" /> Share Allotment</div>
        <div className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-primary-blue" /> Stock Exchange Listing</div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* July Calendar Grid */}
        <div className="lg:col-span-8 bg-card-bg border border-border-strong rounded-lg p-6">
          <div className="grid grid-cols-7 gap-2 mb-4 text-center text-xs font-bold text-text-muted uppercase tracking-wider">
            {daysOfWeek.map(day => <div key={day} className="py-2">{day}</div>)}
          </div>

          <div className="grid grid-cols-7 gap-2">
            {calendarDays.map((day, idx) => {
              if (day === null) {
                return <div key={`empty-${idx}`} className="aspect-square bg-dark-bg/20 rounded border border-transparent" />;
              }

              const hasEvents = events[day] && events[day].length > 0;
              const isSelected = selectedDay === day;

              return (
                <div
                  key={`day-${day}`}
                  onClick={() => setSelectedDay(day)}
                  className={`aspect-square p-2 bg-dark-bg/40 border rounded-md flex flex-col justify-between cursor-pointer transition-all hover:border-primary-blue/50 ${
                    isSelected ? 'border-primary-blue bg-blue-600/5' : 'border-border-strong/40'
                  }`}
                >
                  <span className={`text-xs font-mono font-bold leading-none ${
                    isSelected ? 'text-primary-blue' : 'text-text-secondary'
                  }`}>
                    {day}
                  </span>
                  
                  {hasEvents && (
                    <div className="flex gap-1 flex-wrap overflow-hidden">
                      {events[day].map((ev, evIdx) => (
                        <span
                          key={evIdx}
                          className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                            ev.type === 'open' ? 'bg-accent-emerald' :
                            ev.type === 'close' ? 'bg-red-500' :
                            ev.type === 'allotment' ? 'bg-secondary-purple' : 'bg-primary-blue'
                          }`}
                        />
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Day Details Panel */}
        <div className="lg:col-span-4 bg-card-bg border border-border-strong rounded-lg p-6 flex flex-col justify-between">
          <div className="space-y-6">
            <div className="flex items-center gap-2 text-xs font-semibold text-primary-blue border-b border-border-strong pb-3">
              <CalendarIcon className="w-4 h-4" />
              <span>Schedule Details: July {selectedDay}, 2026</span>
            </div>

            {events[selectedDay] && events[selectedDay].length > 0 ? (
              <div className="space-y-4">
                {events[selectedDay].map((ev, idx) => (
                  <div key={idx} className={`p-4 border border-border-subtle rounded-md bg-dark-bg/60 space-y-2`}>
                    <div className="flex justify-between items-center">
                      <h4 className="text-xs font-bold text-white">{ev.title}</h4>
                      <span className={`text-[8px] font-bold px-2 py-0.5 rounded-full border ${getEventBadgeColor(ev.type)}`}>
                        {ev.type.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-[10px] text-text-secondary leading-relaxed">
                      {ev.type === 'open' && 'Bidding opens today at 10:00 AM. Minimum subscription details listed inside.'}
                      {ev.type === 'close' && 'Bidding closes today at 5:00 PM. Cut-off time for UPI application verification.'}
                      {ev.type === 'allotment' && 'Allotment status check link activated. Enter PAN details to retrieve allotments.'}
                      {ev.type === 'listing' && 'Stock listed on BSE & NSE. Regular market trades begin at 10:00 AM.'}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-16 text-text-muted text-xs flex flex-col items-center gap-2">
                <Info className="w-5 h-5" />
                No scheduled IPO events for this date.
              </div>
            )}
          </div>

          <div className="pt-6 border-t border-border-subtle/30">
            <span className="text-[10px] text-text-muted block text-center">Timelines are subject to change by respective registrar agencies.</span>
          </div>
        </div>

      </div>
    </div>
  );
}
