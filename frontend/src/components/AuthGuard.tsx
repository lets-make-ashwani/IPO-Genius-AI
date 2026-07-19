'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '../context/AuthContext';
import FullScreenLoader from './FullScreenLoader';

interface AuthGuardProps {
  children: React.ReactNode;
  /** If true, only users with role === 'ADMIN' can access the route */
  requireAdmin?: boolean;
}

/**
 * AuthGuard — protects routes that require authentication.
 *
 * Behaviour:
 *  - While session is loading → show FullScreenLoader
 *  - No user → redirect to /login (preserves the intended path via `from` query)
 *  - requireAdmin + non-admin user → redirect to /dashboard
 *  - All checks pass → render children
 *
 * Role is read from the backend JWT (user.role), never inferred from email.
 */
export default function AuthGuard({ children, requireAdmin = false }: AuthGuardProps) {
  const { user, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (loading) return;

    if (!user) {
      // Preserve intended destination so login can redirect back
      router.replace(`/login?from=${encodeURIComponent(pathname)}`);
      return;
    }

    if (requireAdmin && user.role !== 'ADMIN') {
      router.replace('/dashboard');
    }
  }, [user, loading, requireAdmin, router, pathname]);

  // Show spinner while auth state is being determined
  if (loading) {
    return <FullScreenLoader message="Checking session..." />;
  }

  // Render nothing while redirect is in progress
  if (!user) return null;
  if (requireAdmin && user.role !== 'ADMIN') return null;

  return <>{children}</>;
}
