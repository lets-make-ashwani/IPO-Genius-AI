/**
 * api/client.ts — Centralized HTTP client
 *
 * Features:
 * - Base URL from NEXT_PUBLIC_API_URL
 * - Automatic Authorization header injection
 * - Typed JSON responses
 * - 10-second timeout via AbortController
 * - Automatic 401 → refresh → retry flow
 * - Queue-based refresh (one refresh in flight at a time)
 * - Centralized error handling with friendly messages
 * - X-Request-ID header on every request
 *
 * Every service must use apiClient — never call fetch() directly.
 */

import { TokenManager } from '../lib/token.manager';

// ─── Error Type ───────────────────────────────────────────────────────────────

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    message: string,
    public readonly data?: unknown,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// ─── Internal types ───────────────────────────────────────────────────────────

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

interface RequestOptions {
  headers?: Record<string, string>;
  /** Skip attaching the Authorization header (used for login/register/refresh) */
  skipAuth?: boolean;
  /** Internal flag: prevents infinite retry loop after a token refresh */
  _skipRefresh?: boolean;
}

const TIMEOUT_MS = 10_000;

// ─── Client ──────────────────────────────────────────────────────────────────

class ApiClient {
  private readonly baseUrl: string;

  /** True while a refresh call is already in progress */
  private isRefreshing = false;

  /** Callbacks waiting for the in-progress refresh to complete */
  private refreshSubscribers: Array<(token: string | null) => void> = [];

  constructor() {
    this.baseUrl = (process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000').replace(/\/$/, '');
  }

  // ── Refresh queue helpers ─────────────────────────────────────────────────

  private notifyRefreshSubscribers(token: string | null): void {
    this.refreshSubscribers.forEach((cb) => cb(token));
    this.refreshSubscribers = [];
  }

  private waitForRefresh(): Promise<string | null> {
    return new Promise((resolve) => {
      this.refreshSubscribers.push(resolve);
    });
  }

  // ── Token refresh ─────────────────────────────────────────────────────────

  private async attemptTokenRefresh(): Promise<string | null> {
    const refreshToken = TokenManager.getRefreshToken();
    if (!refreshToken) return null;

    // If a refresh is already in flight, queue this caller
    if (this.isRefreshing) {
      return this.waitForRefresh();
    }

    this.isRefreshing = true;

    try {
      const res = await fetch(`${this.baseUrl}/api/v1/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (!res.ok) {
        this.notifyRefreshSubscribers(null);
        return null;
      }

      const json = await res.json();
      const { access_token, refresh_token: newRefresh } = json.data;
      TokenManager.saveTokens(access_token, newRefresh);
      this.notifyRefreshSubscribers(access_token);
      return access_token;
    } catch {
      this.notifyRefreshSubscribers(null);
      return null;
    } finally {
      this.isRefreshing = false;
    }
  }

  // ── Error helpers ─────────────────────────────────────────────────────────

  private extractServerMessage(data: unknown): string {
    if (typeof data !== 'object' || data === null) return '';
    const d = data as Record<string, unknown>;

    if (typeof d.detail === 'string') return d.detail;

    // FastAPI validation error array
    if (Array.isArray(d.detail)) {
      return d.detail
        .map((e: { msg?: string }) => e.msg ?? '')
        .filter(Boolean)
        .join('. ');
    }

    if (typeof d.message === 'string') return d.message;
    return '';
  }

  private toFriendlyMessage(status: number, serverMsg: string): string {
    switch (status) {
      case 401: return 'Invalid email or password.';
      case 403: return 'You do not have permission to perform this action.';
      case 404: return 'The requested resource was not found.';
      case 408: return 'Request timed out. Please try again.';
      case 409: return serverMsg || 'A conflict occurred. Please try again.';
      case 422: return serverMsg || 'Please check your input and try again.';
      case 429: return 'Too many requests. Please wait a moment.';
      default:
        if (status >= 500) return 'Server error. Please try again later.';
        return serverMsg || 'An unexpected error occurred.';
    }
  }

  // ── Core request ─────────────────────────────────────────────────────────

  private async execute<T>(
    method: HttpMethod,
    endpoint: string,
    body?: unknown,
    options: RequestOptions = {},
  ): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

    const requestId =
      typeof crypto !== 'undefined' && crypto.randomUUID
        ? crypto.randomUUID()
        : `${Date.now()}-${Math.random().toString(36).slice(2)}`;

    const accessToken = options.skipAuth ? null : TokenManager.getAccessToken();

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'X-Request-ID': requestId,
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...(options.headers ?? {}),
    };

    const init: RequestInit = {
      method,
      headers,
      signal: controller.signal,
      ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
    };

    try {
      const res = await fetch(`${this.baseUrl}/api/v1${endpoint}`, init);
      clearTimeout(timeoutId);

      // ── 401 → try refresh → retry ────────────────────────────────────────
      if (res.status === 401 && !options._skipRefresh && !options.skipAuth) {
        const newToken = await this.attemptTokenRefresh();

        if (newToken) {
          // Retry with fresh token; _skipRefresh prevents a second retry
          return this.execute<T>(method, endpoint, body, {
            ...options,
            _skipRefresh: true,
          });
        }

        // Refresh failed — clear session and redirect to login
        TokenManager.clearTokens();
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new ApiError(401, 'Session expired. Please sign in again.');
      }

      // ── Non-OK responses ─────────────────────────────────────────────────
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        const serverMsg = this.extractServerMessage(errorData);
        throw new ApiError(
          res.status,
          this.toFriendlyMessage(res.status, serverMsg),
          errorData,
        );
      }

      // ── No-content responses ─────────────────────────────────────────────
      if (res.status === 204) return undefined as unknown as T;

      return (await res.json()) as T;
    } catch (err) {
      clearTimeout(timeoutId);
      if (err instanceof ApiError) throw err;

      if (err instanceof DOMException && err.name === 'AbortError') {
        throw new ApiError(408, 'Request timed out. Please try again.');
      }
      if (err instanceof TypeError) {
        // Network error (offline, DNS failure, etc.)
        throw new ApiError(0, 'Unable to connect. Check your internet connection.');
      }

      throw new ApiError(0, 'An unexpected error occurred.');
    }
  }

  // ── Public HTTP methods ───────────────────────────────────────────────────

  get<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.execute<T>('GET', endpoint, undefined, options);
  }

  post<T>(endpoint: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return this.execute<T>('POST', endpoint, body, options);
  }

  put<T>(endpoint: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return this.execute<T>('PUT', endpoint, body, options);
  }

  patch<T>(endpoint: string, body?: unknown, options?: RequestOptions): Promise<T> {
    return this.execute<T>('PATCH', endpoint, body, options);
  }

  delete<T>(endpoint: string, options?: RequestOptions): Promise<T> {
    return this.execute<T>('DELETE', endpoint, undefined, options);
  }
}

export const apiClient = new ApiClient();
