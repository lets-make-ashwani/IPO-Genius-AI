'use client';

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from 'react';
import { User } from '../types';
import { authService } from '../services/auth.service';

// ─── Context shape ────────────────────────────────────────────────────────────

interface AuthContextValue {
  /** Authenticated user, or null when logged out */
  user: User | null;
  /** True while the initial session check (GET /users/me) is in flight */
  loading: boolean;
  /** Sign in, save tokens, populate user */
  login: (email: string, password: string) => Promise<User>;
  /** Register, auto-login, populate user */
  register: (fullName: string, email: string, password: string) => Promise<User>;
  /** Revoke tokens, clear state, redirect handled by caller */
  logout: () => Promise<void>;
  /** Re-fetch the current user from the API (e.g. after profile update) */
  refresh: () => Promise<void>;
}

// ─── Context ──────────────────────────────────────────────────────────────────

const AuthContext = createContext<AuthContextValue | null>(null);

// ─── Provider ─────────────────────────────────────────────────────────────────

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  /**
   * On mount: attempt to restore the session.
   * If a valid token exists, GET /users/me populates the user.
   * If no token or the token is expired (and refresh fails), user stays null.
   */
  useEffect(() => {
    authService
      .getCurrentUser()
      .then((u) => setUser(u))
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(
    async (email: string, password: string): Promise<User> => {
      const loggedInUser = await authService.login(email, password);
      setUser(loggedInUser);
      return loggedInUser;
    },
    [],
  );

  const register = useCallback(
    async (fullName: string, email: string, password: string): Promise<User> => {
      const newUser = await authService.register(fullName, email, password);
      setUser(newUser);
      return newUser;
    },
    [],
  );

  const logout = useCallback(async (): Promise<void> => {
    await authService.logout();
    setUser(null);
  }, []);

  const refresh = useCallback(async (): Promise<void> => {
    const currentUser = await authService.getCurrentUser();
    setUser(currentUser);
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refresh }}>
      {children}
    </AuthContext.Provider>
  );
}

// ─── Hook ─────────────────────────────────────────────────────────────────────

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth() must be called inside an <AuthProvider>.');
  }
  return ctx;
}
