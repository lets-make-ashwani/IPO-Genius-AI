'use client';

import { useState } from 'react';
import { User, Mail, Phone, MapPin, ShieldAlert, Check } from 'lucide-react';

export default function Profile() {
  const [activeTab, setActiveTab] = useState<'info' | 'password'>('info');
  const [profile, setProfile] = useState({
    name: 'Rahul Kumar',
    email: 'rahul@example.com',
    phone: '+91 98765 43210',
    dob: '1995-08-15',
    city: 'Mumbai',
    state: 'Maharashtra'
  });
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">My Profile</h1>
        <p className="text-xs text-text-muted">Manage your personal credentials and options.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Avatar Card */}
        <div className="lg:col-span-4 bg-card-bg border border-border-strong rounded-lg p-6 flex flex-col items-center text-center space-y-4">
          <div className="w-24 h-24 rounded-full bg-primary-blue/20 flex items-center justify-center font-bold text-primary-blue text-3xl shadow-lg relative cursor-pointer hover:opacity-85 transition-opacity">
            RK
            <span className="absolute bottom-0 right-0 w-7 h-7 bg-primary-blue hover:bg-blue-700 text-white rounded-full flex items-center justify-center border-2 border-card-bg text-xs">
              +
            </span>
          </div>
          <div>
            <h3 className="text-base font-bold text-white leading-tight">{profile.name}</h3>
            <span className="text-[10px] text-text-muted font-mono">{profile.email}</span>
          </div>
          <div className="flex gap-2">
            <span className="text-[10px] font-bold bg-accent-emerald/20 text-accent-emerald px-2 py-0.5 rounded-sm">PRO USER</span>
          </div>

          <div className="w-full pt-4 border-t border-border-subtle/30 grid grid-cols-3 gap-2 text-center text-xs">
            <div>
              <span className="text-[10px] text-text-muted block">WATCHED</span>
              <span className="font-bold text-white font-mono">3</span>
            </div>
            <div>
              <span className="text-[10px] text-text-muted block">REPORTS</span>
              <span className="font-bold text-white font-mono">12</span>
            </div>
            <div>
              <span className="text-[10px] text-text-muted block">ALERTS</span>
              <span className="font-bold text-white font-mono">5</span>
            </div>
          </div>
        </div>

        {/* Right Form Card */}
        <div className="lg:col-span-8 bg-card-bg border border-border-strong rounded-lg overflow-hidden">
          <div className="flex border-b border-border-strong bg-dark-bg/20 text-xs font-bold uppercase tracking-wider text-text-secondary">
            <button
              onClick={() => setActiveTab('info')}
              className={`px-6 py-4 transition-colors ${activeTab === 'info' ? 'text-white border-b-2 border-primary-blue bg-card-bg' : 'hover:text-white'}`}
            >
              Personal Info
            </button>
            <button
              onClick={() => setActiveTab('password')}
              className={`px-6 py-4 transition-colors ${activeTab === 'password' ? 'text-white border-b-2 border-primary-blue bg-card-bg' : 'hover:text-white'}`}
            >
              Change Password
            </button>
          </div>

          <div className="p-6">
            {activeTab === 'info' ? (
              <form onSubmit={handleSave} className="space-y-6">
                {saved && (
                  <div className="p-3 bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald rounded-md text-xs flex items-center gap-2">
                    <Check className="w-4 h-4" /> Changes saved successfully!
                  </div>
                )}

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">Full Name</label>
                    <input
                      type="text"
                      value={profile.name}
                      onChange={(e) => setProfile(p => ({ ...p, name: e.target.value }))}
                      className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">Email Address</label>
                    <input
                      disabled
                      type="email"
                      value={profile.email}
                      className="w-full h-10 px-4 rounded-md bg-dark-bg/40 border border-border-subtle/50 text-xs text-text-muted cursor-not-allowed"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">Phone Number</label>
                    <input
                      type="text"
                      value={profile.phone}
                      onChange={(e) => setProfile(p => ({ ...p, phone: e.target.value }))}
                      className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">Date of Birth</label>
                    <input
                      type="date"
                      value={profile.dob}
                      onChange={(e) => setProfile(p => ({ ...p, dob: e.target.value }))}
                      className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all text-text-secondary"
                    />
                  </div>
                </div>

                <div className="flex justify-end pt-4 border-t border-border-subtle/25">
                  <button type="submit" className="bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs px-5 py-2.5 rounded-md shadow-md transition-colors">
                    Save Changes
                  </button>
                </div>
              </form>
            ) : (
              /* Password change */
              <form onSubmit={handleSave} className="space-y-6">
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">Current Password</label>
                    <input type="password" placeholder="••••••••" className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all" />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">New Password</label>
                    <input type="password" placeholder="Min. 8 characters" className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all" />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">Confirm New Password</label>
                    <input type="password" placeholder="••••••••" className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all" />
                  </div>
                </div>

                <div className="flex justify-end pt-4 border-t border-border-subtle/25">
                  <button type="submit" className="bg-primary-blue hover:bg-blue-700 text-white font-semibold text-xs px-5 py-2.5 rounded-md shadow-md transition-colors">
                    Update Password
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
