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
   * Update authenticated user profile name
   */
  async updateProfile(fullName: string): Promise<User | null> {
    try {
      const response = await apiClient.put<BackendApiResponse<BackendUser>>('/users/me', {
        full_name: fullName
      });
      if (!response.data) return null;
      return toFrontendUser(response.data);
    } catch (error) {
      console.error('Failed to update profile:', error);
      throw error;
    }
  },

  /**
   * Change user password
   */
  async changePassword(oldPassword: string, newPassword: string): Promise<void> {
    try {
      await apiClient.put<BackendApiResponse<null>>('/users/me/password', {
        old_password: oldPassword,
        new_password: newPassword
      });
    } catch (error) {
      console.error('Failed to change password:', error);
      throw error;
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
