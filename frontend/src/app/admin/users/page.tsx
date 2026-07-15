'use client';

import { useState } from 'react';
import { 
  Users as UsersIcon, 
  Search, 
  ShieldAlert, 
  Check, 
  DollarSign, 
  CreditCard,
  Ban,
  RotateCcw,
  Download
} from 'lucide-react';
import { mockUsers, mockTransactions } from '../../../constants/mockData';
import { User, Transaction } from '../../../types';
import { userService } from '../../../services/user.service';

export default function UserManagement() {
  const [users, setUsers] = useState<User[]>(mockUsers);
  const [transactions, setTransactions] = useState<Transaction[]>(mockTransactions);
  const [userSearch, setUserSearch] = useState('');
  const [txSearch, setTxSearch] = useState('');
  const [activeSubTab, setActiveSubTab] = useState<'users' | 'payments'>('users');

  const [message, setMessage] = useState<string | null>(null);

  const handleBlockUser = async (userId: string, currentStatus: User['status']) => {
    const nextStatus: User['status'] = currentStatus === 'Active' ? 'Blocked' : 'Active';
    const updated = await userService.updateUserStatus(userId, nextStatus);
    setUsers((prev) => prev.map((u) => (u.id === userId ? updated : u)));
    setMessage(`User ${updated.name} status updated to ${updated.status}.`);
    setTimeout(() => setMessage(null), 2000);
  };

  const handleRefund = async (txId: string) => {
    if (confirm('Are you sure you want to refund this transaction?')) {
      const updated = await userService.refundTransaction(txId);
      setTransactions((prev) => prev.map((t) => (t.id === txId ? updated : t)));
      setMessage(`Transaction ${txId} successfully refunded.`);
      setTimeout(() => setMessage(null), 2000);
    }
  };

  const filteredUsers = users.filter(
    (u) => u.name.toLowerCase().includes(userSearch.toLowerCase()) || u.email.toLowerCase().includes(userSearch.toLowerCase())
  );

  const filteredTransactions = transactions.filter(
    (t) => t.id.toLowerCase().includes(txSearch.toLowerCase()) || t.userName.toLowerCase().includes(txSearch.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">Accounts & Billings</h1>
        <p className="text-xs text-text-muted">Audit system user profiles, subscription plans, and invoice history.</p>
      </div>

      {message && (
        <div className="p-3 bg-accent-emerald/10 border border-accent-emerald/20 text-accent-emerald rounded-md text-xs flex items-center gap-2">
          <Check className="w-4 h-4" /> {message}
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b border-border-strong gap-8 text-sm font-semibold">
        <button
          onClick={() => setActiveSubTab('users')}
          className={`pb-3 border-b-2 transition-all ${
            activeSubTab === 'users' ? 'border-primary-blue text-primary-blue' : 'border-transparent text-text-muted hover:text-white'
          }`}
        >
          User Directory ({users.length})
        </button>
        <button
          onClick={() => setActiveSubTab('payments')}
          className={`pb-3 border-b-2 transition-all ${
            activeSubTab === 'payments' ? 'border-primary-blue text-primary-blue' : 'border-transparent text-text-muted hover:text-white'
          }`}
        >
          Transactions Log ({transactions.length})
        </button>
      </div>

      {activeSubTab === 'users' ? (
        /* Users List Tab */
        <div className="space-y-4">
          <div className="relative w-80">
            <Search className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
            <input
              type="text"
              placeholder="Search user profiles..."
              value={userSearch}
              onChange={(e) => setUserSearch(e.target.value)}
              className="w-full h-10 pl-10 pr-4 rounded-md bg-card-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all"
            />
          </div>

          <div className="bg-card-bg border border-border-strong rounded-lg overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-border-strong bg-dark-bg/40 font-bold text-text-muted uppercase tracking-wider">
                  <th className="p-4 pl-6">User</th>
                  <th className="p-4">Email</th>
                  <th className="p-4">Plan</th>
                  <th className="p-4">Status</th>
                  <th className="p-4">Joined Date</th>
                  <th className="p-4 pr-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="text-text-secondary divide-y divide-border-strong/30">
                {filteredUsers.map((u) => (
                  <tr key={u.id} className="hover:bg-dark-bg/25 transition-colors">
                    <td className="p-4 pl-6 flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-primary-blue/20 flex items-center justify-center font-bold text-primary-blue">{u.avatar}</div>
                      <span className="font-bold text-white">{u.name}</span>
                    </td>
                    <td className="p-4 font-mono">{u.email}</td>
                    <td className="p-4">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                        u.plan === 'Pro' ? 'bg-primary-blue/10 text-primary-blue' :
                        u.plan === 'Enterprise' ? 'bg-secondary-purple/10 text-secondary-purple' :
                        'bg-border-subtle text-text-secondary'
                      }`}>{u.plan}</span>
                    </td>
                    <td className="p-4">
                      <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
                        u.status === 'Active' ? 'bg-accent-emerald/10 text-accent-emerald' : 'bg-red-500/10 text-red-400'
                      }`}>{u.status.toUpperCase()}</span>
                    </td>
                    <td className="p-4 font-mono">{u.joinedDate}</td>
                    <td className="p-4 pr-6 text-right flex justify-end gap-3">
                      <button onClick={() => handleBlockUser(u.id, u.status)} className="p-1.5 rounded hover:bg-red-500/10 text-text-muted hover:text-red-400 transition-colors" title={u.status === 'Active' ? 'Block user' : 'Unblock user'}><Ban className="w-4 h-4" /></button>
                      <button className="p-1.5 rounded hover:bg-border-subtle text-text-muted hover:text-white transition-colors" title="Reset password"><RotateCcw className="w-4 h-4" /></button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        /* Payments Transactions Tab */
        <div className="space-y-4">
          <div className="relative w-80">
            <Search className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
            <input
              type="text"
              placeholder="Search transaction log..."
              value={txSearch}
              onChange={(e) => setTxSearch(e.target.value)}
              className="w-full h-10 pl-10 pr-4 rounded-md bg-card-bg border border-border-subtle focus:border-primary-blue text-xs focus:outline-none text-white focus:ring-1 focus:ring-primary-blue transition-all"
            />
          </div>

          <div className="bg-card-bg border border-border-strong rounded-lg overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-border-strong bg-dark-bg/40 font-bold text-text-muted uppercase tracking-wider">
                  <th className="p-4 pl-6">Transaction ID</th>
                  <th className="p-4">Customer Name</th>
                  <th className="p-4">Billing Amount</th>
                  <th className="p-4">Date</th>
                  <th className="p-4">Status</th>
                  <th className="p-4 pr-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="text-text-secondary divide-y divide-border-strong/30">
                {filteredTransactions.map((tx) => (
                  <tr key={tx.id} className="hover:bg-dark-bg/25 transition-colors">
                    <td className="p-4 pl-6 font-bold text-white font-mono">{tx.id}</td>
                    <td className="p-4 font-semibold">{tx.userName}</td>
                    <td className="p-4 font-mono font-semibold text-white">₹{tx.amount}</td>
                    <td className="p-4 font-mono">{tx.date}</td>
                    <td className="p-4">
                      <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
                        tx.status === 'Success' ? 'bg-accent-emerald/10 text-accent-emerald' :
                        tx.status === 'Failed' ? 'bg-red-500/10 text-red-400' :
                        'bg-border-subtle text-text-secondary'
                      }`}>{tx.status.toUpperCase()}</span>
                    </td>
                    <td className="p-4 pr-6 text-right flex justify-end gap-3">
                      {tx.status === 'Success' && (
                        <button onClick={() => handleRefund(tx.id)} className="h-7 px-3 border border-border-subtle hover:bg-dark-bg text-[10px] font-semibold text-white rounded transition-colors">
                          Refund
                        </button>
                      )}
                      <button className="p-1.5 rounded hover:bg-border-subtle text-text-muted hover:text-white transition-colors" title="Download invoice"><Download className="w-3.5 h-3.5" /></button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
