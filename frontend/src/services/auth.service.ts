/**
 * auth.service.ts — Real authentication service
 *
 * Replaces the previous mock implementation.
 * All methods call the live FastAPI backend via apiClient.
 * Token persistence is handled by TokenManager.
 * Type mapping is handled by toFrontendUser().
 *
 * This module is a pure API call layer — it holds no state.
 * Auth state (user object, loading) lives in AuthContext.
 */

import { apiClient } from '../api/client';
import { TokenManager } from '../lib/token.manager';
import { toFrontendUser } from '../lib/auth.adapter';
import { User } from '../types';
import { BackendApiResponse, BackendTokenData, BackendUser } from '../types/api';

export const authService = {
  /**
   * Sign in with email and password.
   * Saves access + refresh tokens on success.
   * Returns the adapted frontend User.
   */
  async login(email: string, password: string): Promise<User> {
    const response = await apiClient.post<BackendApiResponse<BackendTokenData>>(
      '/auth/login',
      { email, password },
      { skipAuth: true },
    );

    const { access_token, refresh_token, user } = response.data!;
    TokenManager.saveTokens(access_token, refresh_token);
    return toFrontendUser(user);
  },

  /**
   * Create a new account then auto-login.
   * The backend does not return tokens on register, so we call login after.
   */
  async register(fullName: string, email: string, password: string): Promise<User> {
    await apiClient.post<BackendApiResponse>(
      '/auth/register',
      { full_name: fullName, email, password },
      { skipAuth: true },
    );
    // Auto-login so the user lands in the app immediately
    return this.login(email, password);
  },

  /**
   * Fetch the current user from GET /users/me.
   * Returns null if no token exists or the request fails.
   * Used by AuthContext on startup to restore the session.
   */
  async getCurrentUser(): Promise<User | null> {
    if (!TokenManager.isLoggedIn()) return null;

    try {
      const response = await apiClient.get<BackendApiResponse<BackendUser>>('/users/me');
      return toFrontendUser(response.data!);
    } catch {
      // Token may be expired; the ApiClient will have already attempted a refresh.
      // If we reach here, the session is truly gone.
      return null;
    }
  },

  /**
   * Sign out the current user.
   * Calls POST /auth/logout to revoke the refresh token server-side.
   * Always clears local tokens even if the network request fails.
   */
  async logout(): Promise<void> {
    const refreshToken = TokenManager.getRefreshToken();
    try {
      if (refreshToken) {
        await apiClient.post('/auth/logout', { refresh_token: refreshToken });
      }
    } finally {
      // Always clear tokens locally — even if the server call fails
      TokenManager.clearTokens();
    }
  },

  /**
   * Send a password reset link to the provided email.
   * The backend currently mocks this — it always returns success.
   */
  async sendPasswordReset(email: string): Promise<boolean> {
    await apiClient.post(
      '/auth/forgot-password',
      { email },
      { skipAuth: true },
    );
    return true;
  },

  /**
   * Submit the new password and the reset token to the backend.
   */
  async resetPassword(token: string, newPassword: string): Promise<boolean> {
    await apiClient.post(
      '/auth/reset-password',
      { token, new_password: newPassword },
      { skipAuth: true },
    );
    return true;
  },
};

