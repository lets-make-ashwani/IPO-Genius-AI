import { User } from '../types';
import { mockUsers } from '../constants/mockData';

let currentUser: User | null = mockUsers[0]; // Prefill with Rahul Kumar

export const authService = {
  getCurrentUser: async (): Promise<User | null> => {
    return currentUser;
  },

  login: async (email: string, password: string): Promise<User> => {
    await new Promise((resolve) => setTimeout(resolve, 800));
    
    // Simple mock check
    if (password === 'error') {
      throw new Error('Incorrect password. Please try again.');
    }
    
    const user = mockUsers.find((u) => u.email === email) || {
      id: 'mock-user',
      name: email.split('@')[0],
      email: email,
      avatar: email.substring(0, 2).toUpperCase(),
      plan: 'Free' as const,
      status: 'Active' as const,
      joinedDate: 'Today'
    };
    
    currentUser = user;
    return user;
  },

  register: async (name: string, email: string): Promise<User> => {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    const user: User = {
      id: 'u-' + Math.random().toString(36).substr(2, 9),
      name,
      email,
      avatar: name.substring(0, 2).toUpperCase(),
      plan: 'Free',
      status: 'Active',
      joinedDate: 'Today'
    };
    currentUser = user;
    return user;
  },

  logout: async (): Promise<void> => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    currentUser = null;
  },

  sendPasswordReset: async (email: string): Promise<boolean> => {
    await new Promise((resolve) => setTimeout(resolve, 600));
    return true;
  },

  resetPassword: async (): Promise<boolean> => {
    await new Promise((resolve) => setTimeout(resolve, 800));
    return true;
  },

  verifyEmail: async (otp: string): Promise<boolean> => {
    await new Promise((resolve) => setTimeout(resolve, 500));
    return otp === '123456' || otp.length === 6;
  }
};
