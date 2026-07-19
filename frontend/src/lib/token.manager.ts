/**
 * TokenManager — single source of truth for JWT token storage.
 *
 * All localStorage access MUST go through this module.
 * Never call localStorage.getItem/setItem for tokens anywhere else.
 */

const ACCESS_TOKEN_KEY = 'ipo_access_token';
const REFRESH_TOKEN_KEY = 'ipo_refresh_token';

const isBrowser = typeof window !== 'undefined';

export const TokenManager = {
  /** Persist both tokens at once (call after login or refresh) */
  saveTokens(accessToken: string, refreshToken: string): void {
    if (!isBrowser) return;
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  },

  saveAccessToken(token: string): void {
    if (!isBrowser) return;
    localStorage.setItem(ACCESS_TOKEN_KEY, token);
  },

  saveRefreshToken(token: string): void {
    if (!isBrowser) return;
    localStorage.setItem(REFRESH_TOKEN_KEY, token);
  },

  getAccessToken(): string | null {
    if (!isBrowser) return null;
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  },

  getRefreshToken(): string | null {
    if (!isBrowser) return null;
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  },

  /** Remove both tokens — call on logout or session expiry */
  clearTokens(): void {
    if (!isBrowser) return;
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  },

  /** Returns true if an access token exists (not validated, just present) */
  isLoggedIn(): boolean {
    return !!this.getAccessToken();
  },

  /** Returns the Authorization header object, or empty object if no token */
  getAuthHeader(): Record<string, string> {
    const token = this.getAccessToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  },
};
