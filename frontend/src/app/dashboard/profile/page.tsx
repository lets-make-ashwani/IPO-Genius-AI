'use client';

import { useState, useEffect } from 'react';
import { ShieldAlert, Check } from 'lucide-react';
import { useAuth } from '../../../context/AuthContext';
import { userService } from '../../../services/user.service';

export default function Profile() {
  const { user, refresh } = useAuth();
  const [activeTab, setActiveTab] = useState<'info' | 'password'>('info');
  
  // Profile form state
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    phone: '+91 98765 43210', // Static presentation field
    dob: '1995-08-15',      // Static presentation field
  });
  
  // Password change state
  const [passwords, setPasswords] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [submitting, setSubmitting] = useState(false);

  // Sync profile state with logged-in user context
  useEffect(() => {
    if (user) {
      setProfile(p => ({
        ...p,
        name: user.name || '',
        email: user.email || '',
      }));
    }
  }, [user]);

  // Handle personal info saving
  const handleSaveInfo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!profile.name.trim()) {
      setMessage({ type: 'error', text: 'Full Name cannot be empty.' });
      return;
    }
    setSubmitting(true);
    setMessage(null);
    try {
      await userService.updateProfile(profile.name);
      await refresh(); // Refresh user in context (updates Header, Sidebar etc.)
      setMessage({ type: 'success', text: 'Profile changes saved successfully!' });
    } catch (err: any) {
      console.error(err);
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to update profile. Please try again.' });
    } finally {
      setSubmitting(false);
    }
  };

  // Handle password changing
  const handleSavePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!passwords.oldPassword || !passwords.newPassword) {
      setMessage({ type: 'error', text: 'Please fill in both current and new password fields.' });
      return;
    }
    if (passwords.newPassword.length < 6) {
      setMessage({ type: 'error', text: 'New password must be at least 6 characters.' });
      return;
    }
    if (passwords.newPassword !== passwords.confirmPassword) {
      setMessage({ type: 'error', text: 'New passwords do not match.' });
      return;
    }

    setSubmitting(true);
    setMessage(null);
    try {
      await userService.changePassword(passwords.oldPassword, passwords.newPassword);
      setMessage({ type: 'success', text: 'Password updated successfully!' });
      setPasswords({ oldPassword: '', newPassword: '', confirmPassword: '' });
    } catch (err: any) {
      console.error(err);
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to change password. Please verify current credentials.' });
    } finally {
      setSubmitting(false);
    }
  };

  // Get user name initials for avatar icon
  const initials = user?.name 
    ? user.name.split(' ').map(n => n.charAt(0)).join('').toUpperCase().slice(0, 2)
    : 'U';

  const userRole = user?.role || 'USER';

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
            {initials}
            <span className="absolute bottom-0 right-0 w-7 h-7 bg-primary-blue hover:bg-blue-700 text-white rounded-full flex items-center justify-center border-2 border-card-bg text-xs">
              +
            </span>
          </div>
          <div>
            <h3 className="text-base font-bold text-white leading-tight">{profile.name || 'Investor'}</h3>
            <span className="text-[10px] text-text-muted font-mono">{profile.email}</span>
          </div>
          <div className="flex gap-2">
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-sm ${
              userRole === 'ADMIN' ? 'bg-secondary-purple/20 text-secondary-purple' : 'bg-accent-emerald/20 text-accent-emerald'
            }`}>
              {userRole.toUpperCase()} USER
            </span>
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
              onClick={() => { setActiveTab('info'); setMessage(null); }}
              className={`px-6 py-4 transition-colors ${activeTab === 'info' ? 'text-white border-b-2 border-primary-blue bg-card-bg' : 'hover:text-white'}`}
            >
              Personal Info
            </button>
            <button
              onClick={() => { setActiveTab('password'); setMessage(null); }}
              className={`px-6 py-4 transition-colors ${activeTab === 'password' ? 'text-white border-b-2 border-primary-blue bg-card-bg' : 'hover:text-white'}`}
            >
              Change Password
            </button>
          </div>

          <div className="p-6">
            {message && (
              <div className={`p-3 mb-6 border rounded-md text-xs flex items-center gap-2 ${
                message.type === 'success' 
                  ? 'bg-accent-emerald/10 border-accent-emerald/20 text-accent-emerald' 
                  : 'bg-red-500/10 border-red-500/20 text-red-400'
              }`}>
                {message.type === 'success' ? <Check className="w-4 h-4" /> : <ShieldAlert className="w-4 h-4" />}
                {message.text}
              </div>
            )}

            {activeTab === 'info' ? (
              <form onSubmit={handleSaveInfo} className="space-y-6">
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
                  <button 
                    type="submit" 
                    disabled={submitting}
                    className="bg-primary-blue hover:bg-blue-700 disabled:opacity-50 text-white font-semibold text-xs px-5 py-2.5 rounded-md shadow-md transition-colors"
                  >
                    {submitting ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </form>
            ) : (
              /* Password change */
              <form onSubmit={handleSavePassword} className="space-y-6">
                <div className="space-y-4">
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">Current Password</label>
                    <input 
                      type="password" 
                      placeholder="••••••••" 
                      value={passwords.oldPassword}
                      onChange={(e) => setPasswords(p => ({ ...p, oldPassword: e.target.value }))}
                      className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all" 
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">New Password</label>
                    <input 
                      type="password" 
                      placeholder="Min. 6 characters" 
                      value={passwords.newPassword}
                      onChange={(e) => setPasswords(p => ({ ...p, newPassword: e.target.value }))}
                      className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all" 
                    />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-bold text-text-muted uppercase">Confirm New Password</label>
                    <input 
                      type="password" 
                      placeholder="••••••••" 
                      value={passwords.confirmPassword}
                      onChange={(e) => setPasswords(p => ({ ...p, confirmPassword: e.target.value }))}
                      className="w-full h-10 px-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all" 
                    />
                  </div>
                </div>

                <div className="flex justify-end pt-4 border-t border-border-subtle/25">
                  <button 
                    type="submit" 
                    disabled={submitting}
                    className="bg-primary-blue hover:bg-blue-700 disabled:opacity-50 text-white font-semibold text-xs px-5 py-2.5 rounded-md shadow-md transition-colors"
                  >
                    {submitting ? 'Updating...' : 'Update Password'}
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
