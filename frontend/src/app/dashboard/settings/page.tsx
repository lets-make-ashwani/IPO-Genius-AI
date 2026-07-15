'use client';

import { useState } from 'react';
import { Settings as SettingsIcon, Bell, Shield, Keyboard, Check } from 'lucide-react';

export default function Settings() {
  const [activeTab, setActiveTab] = useState<'notifications' | 'preferences'>('notifications');
  const [saved, setSaved] = useState(false);

  const [notifs, setNotifs] = useState({
    emailOpen: true,
    emailClose: true,
    telegramOpen: false,
    telegramClose: false,
    aiUpdate: true,
    weeklyDigest: true
  });

  const handleToggle = (key: keyof typeof notifs) => {
    setNotifs(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">System Settings</h1>
        <p className="text-xs text-text-muted">Manage notification rules and system preferences.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left categories navigation */}
        <div className="lg:col-span-3 bg-card-bg border border-border-strong rounded-lg p-4 h-fit">
          <ul className="space-y-1 text-xs font-semibold">
            <li>
              <button
                onClick={() => setActiveTab('notifications')}
                className={`w-full text-left px-3 py-2 rounded-md flex items-center gap-2.5 transition-colors ${
                  activeTab === 'notifications' ? 'bg-blue-600/10 text-primary-blue' : 'text-text-secondary hover:bg-dark-bg/60 hover:text-white'
                }`}
              >
                <Bell className="w-4 h-4" /> Notifications Settings
              </button>
            </li>
            <li>
              <button
                onClick={() => setActiveTab('preferences')}
                className={`w-full text-left px-3 py-2 rounded-md flex items-center gap-2.5 transition-colors ${
                  activeTab === 'preferences' ? 'bg-blue-600/10 text-primary-blue' : 'text-text-secondary hover:bg-dark-bg/60 hover:text-white'
                }`}
              >
                <SettingsIcon className="w-4 h-4" /> Preferences
              </button>
            </li>
          </ul>
        </div>

        {/* Right Settings Form */}
        <div className="lg:col-span-9 bg-card-bg border border-border-strong rounded-lg p-6 space-y-6">
          {saved && (
            <div className="p-3 bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald rounded-md text-xs flex items-center gap-2">
              <Check className="w-4 h-4" /> Settings updated successfully!
            </div>
          )}

          {activeTab === 'notifications' ? (
            <div className="space-y-6">
              <h3 className="font-bold text-white text-sm border-b border-border-strong pb-3">Notification Preferences</h3>
              
              <div className="space-y-6">
                {[
                  { label: 'IPO Opening Alerts', desc: 'Receive email alerts when a watched IPO opens for subscription.', value: notifs.emailOpen, key: 'emailOpen' as const },
                  { label: 'IPO Closing Reminders', desc: 'Get reminded 2 hours before bidding window closes.', value: notifs.emailClose, key: 'emailClose' as const },
                  { label: 'Telegram Opening Broadcasts', desc: 'Forward subscription alerts directly to your Telegram chat.', value: notifs.telegramOpen, key: 'telegramOpen' as const, telegram: true },
                  { label: 'Telegram Closing Broadcasts', desc: 'Get Telegram notifications for active closing IPO bidding hours.', value: notifs.telegramClose, key: 'telegramClose' as const, telegram: true },
                  { label: 'AI Score Updates', desc: 'Receive email notifications when AI models regenerate stock ratings.', value: notifs.aiUpdate, key: 'aiUpdate' as const },
                  { label: 'Weekly Performance Digest', desc: 'Consolidated weekly emails tracking listing day outcomes.', value: notifs.weeklyDigest, key: 'weeklyDigest' as const }
                ].map((row, idx) => (
                  <div key={idx} className="flex justify-between items-start gap-4">
                    <div className="text-left">
                      <span className="text-xs font-bold text-white block mb-0.5">{row.label}</span>
                      <span className="text-[10px] text-text-secondary leading-relaxed block max-w-lg">{row.desc}</span>
                      {row.telegram && !row.value && (
                        <span className="text-[9px] text-primary-blue font-bold hover:underline block mt-1 cursor-pointer">Connect Telegram account →</span>
                      )}
                    </div>
                    <button
                      onClick={() => handleToggle(row.key)}
                      className={`w-11 h-6 rounded-full p-0.5 shrink-0 transition-colors ${row.value ? 'bg-primary-blue' : 'bg-dark-bg border border-border-subtle'}`}
                    >
                      <div className={`w-5 h-5 rounded-full bg-white transition-all ${row.value ? 'translate-x-5' : ''}`} />
                    </button>
                  </div>
                ))}
              </div>

              <div className="flex justify-end pt-4 border-t border-border-subtle/25">
                <button onClick={handleSave} className="bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs px-5 py-2.5 rounded-md shadow-md transition-colors">
                  Save Preferences
                </button>
              </div>
            </div>
          ) : (
            /* General Preferences */
            <div className="space-y-6">
              <h3 className="font-bold text-white text-sm border-b border-border-strong pb-3">General Preferences</h3>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-xs">
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold text-text-muted uppercase">Default Language</label>
                  <select className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none text-text-secondary focus:ring-1 focus:ring-primary-blue">
                    <option>English</option>
                    <option>Hindi</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] font-bold text-text-muted uppercase">Default Region</label>
                  <select className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue focus:outline-none text-text-secondary focus:ring-1 focus:ring-primary-blue">
                    <option>India (IST)</option>
                    <option>Global (UTC)</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end pt-4 border-t border-border-subtle/25">
                <button onClick={handleSave} className="bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs px-5 py-2.5 rounded-md shadow-md transition-colors">
                  Save Changes
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
