'use client';

import { useState } from 'react';
import { 
  Users as UsersIcon, 
  Search, 
  ShieldAlert, 
  Check, 
  DollarSign
} from 'lucide-react';
import { useAuth } from '../../../context/AuthContext';

export default function UserManagement() {
  const { user } = useAuth();
  const [search, setSearch] = useState('');

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Accounts & User Management</h1>
        <p className="text-xs text-text-muted">Audit system user profiles, RBAC roles, and authentication sessions.</p>
      </div>

      {/* Admin User Profile Overview Card */}
      <div className="p-6 bg-card-bg border border-border-strong rounded-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-gradient-to-br from-primary-blue to-secondary-purple flex items-center justify-center font-bold text-white text-xl">
            {user?.name ? user.name.charAt(0).toUpperCase() : 'A'}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-white">{user?.name || 'Administrator'}</h2>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-secondary-purple/10 text-secondary-purple border border-secondary-purple/20">
                {user?.role || 'ADMIN'}
              </span>
            </div>
            <p className="text-xs text-text-muted mt-1">{user?.email || 'admin@ipogenius.ai'}</p>
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs font-mono">
          <span className="p-2 rounded bg-dark-bg border border-border-subtle text-accent-emerald">
            JWT Session Active
          </span>
        </div>
      </div>

      {/* Users Table */}
      <div className="bg-card-bg border border-border-strong rounded-lg overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-border-strong bg-dark-bg/60 text-text-muted uppercase text-[10px] font-mono">
              <th className="p-4">User Name</th>
              <th className="p-4">Email Address</th>
              <th className="p-4">Role</th>
              <th className="p-4">Status</th>
              <th className="p-4 text-right">Session Token</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-subtle/40 text-text-secondary">
            <tr className="hover:bg-dark-bg/30 transition-colors">
              <td className="p-4 font-semibold text-white">{user?.name || 'Admin User'}</td>
              <td className="p-4 font-mono">{user?.email || 'admin@ipogenius.ai'}</td>
              <td className="p-4">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-primary-blue/10 text-primary-blue border border-primary-blue/20">
                  {user?.role || 'ADMIN'}
                </span>
              </td>
              <td className="p-4">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-accent-emerald/10 text-accent-emerald border border-accent-emerald/20">
                  ACTIVE
                </span>
              </td>
              <td className="p-4 text-right font-mono text-text-muted">HS256 Verified</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
