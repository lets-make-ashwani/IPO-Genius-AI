import { User, Transaction } from '../types';
import { mockUsers, mockTransactions } from '../constants/mockData';

let users: User[] = [...mockUsers];
let transactions: Transaction[] = [...mockTransactions];

export const userService = {
  getUsers: async (search?: string, plan?: string, status?: string): Promise<User[]> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    let filtered = [...users];

    if (search) {
      const s = search.toLowerCase();
      filtered = filtered.filter((u) => u.name.toLowerCase().includes(s) || u.email.toLowerCase().includes(s));
    }

    if (plan && plan !== 'All') {
      filtered = filtered.filter((u) => u.plan.toLowerCase() === plan.toLowerCase());
    }

    if (status && status !== 'All') {
      filtered = filtered.filter((u) => u.status.toLowerCase() === status.toLowerCase());
    }

    return filtered;
  },

  updateUserPlan: async (userId: string, plan: User['plan']): Promise<User> => {
    await new Promise((resolve) => setTimeout(resolve, 400));
    users = users.map((u) => (u.id === userId ? { ...u, plan } : u));
    const found = users.find((u) => u.id === userId);
    if (!found) throw new Error('User not found');
    return found;
  },

  updateUserStatus: async (userId: string, status: User['status']): Promise<User> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    users = users.map((u) => (u.id === userId ? { ...u, status } : u));
    const found = users.find((u) => u.id === userId);
    if (!found) throw new Error('User not found');
    return found;
  },

  getTransactions: async (search?: string, status?: string): Promise<Transaction[]> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    let filtered = [...transactions];

    if (search) {
      const s = search.toLowerCase();
      filtered = filtered.filter((t) => t.id.toLowerCase().includes(s) || t.userName.toLowerCase().includes(s));
    }

    if (status && status !== 'All') {
      filtered = filtered.filter((t) => t.status.toLowerCase() === status.toLowerCase());
    }

    return filtered;
  },

  refundTransaction: async (txId: string): Promise<Transaction> => {
    await new Promise((resolve) => setTimeout(resolve, 500));
    transactions = transactions.map((t) => (t.id === txId ? { ...t, status: 'Refunded' } : t));
    const found = transactions.find((t) => t.id === txId);
    if (!found) throw new Error('Transaction not found');
    return found;
  }
};
