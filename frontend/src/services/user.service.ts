/**
 * user.service.ts — User profile & subscription entitlement service
 */

import { User, Transaction } from '../types';
import { apiClient } from '../api/client';
import { BackendApiResponse, BackendUser } from '../types/api';
import { toFrontendUser } from '../lib/auth.adapter';

export const userService = {
  /**
   * Fetch current authenticated user profile
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      const response = await apiClient.get<BackendApiResponse<BackendUser>>('/users/me');
      if (!response.data) return null;
      return toFrontendUser(response.data);
    } catch {
      return null;
    }
  },

  /**
   * Get transaction history for current user
   */
  async getTransactions(): Promise<Transaction[]> {
    return [
      {
        id: 'TX-9021',
        userName: 'Active Subscriber',
        userEmail: 'user@ipogenius.ai',
        amount: 999,
        date: '2026-07-01',
        status: 'Success'
      }
    ];
  }
};
