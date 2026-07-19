/**
 * auth.adapter.ts
 *
 * Maps backend UserResponse (snake_case) → frontend User (camelCase).
 *
 * Rules:
 * - `role` is the RBAC concept — mapped directly, never converted to a plan tier
 * - `plan` is the billing/subscription tier — defaults to 'Free' until billing is wired
 * - `avatar` falls back to initials from full_name if avatar_url is null
 */

import { User } from '../types';
import { BackendUser } from '../types/api';

/** Generate two-letter initials from a full name */
function buildInitials(fullName: string): string {
  return fullName
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((word) => word.charAt(0).toUpperCase())
    .join('');
}

/** Format ISO datetime → "19 Jul 2026" */
function formatJoinedDate(isoDate: string): string {
  try {
    return new Date(isoDate).toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  } catch {
    return isoDate;
  }
}

/**
 * Convert a backend UserResponse into the frontend User shape.
 * This is the ONLY place where field name mapping should happen.
 */
export function toFrontendUser(backendUser: BackendUser): User {
  return {
    id: String(backendUser.id),
    name: backendUser.full_name,
    email: backendUser.email,
    // Use avatar_url if provided; otherwise generate initials
    avatar: backendUser.avatar_url ?? buildInitials(backendUser.full_name),
    // Role is the backend RBAC concept — kept as-is, not converted to plan
    role: backendUser.role,
    // Subscription plan defaults to Free until billing module is wired
    plan: 'Free',
    status: backendUser.is_active ? 'Active' : 'Blocked',
    joinedDate: formatJoinedDate(backendUser.created_at),
  };
}
