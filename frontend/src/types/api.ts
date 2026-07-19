/**
 * Backend API response types.
 * These mirror the FastAPI Pydantic schemas exactly.
 * Never use these directly in UI — always pass through auth.adapter.ts first.
 */

/** Shape of every backend API response envelope */
export interface BackendApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T;
}

/** UserResponse from the backend (fields use snake_case) */
export interface BackendUser {
  id: string;
  full_name: string;
  email: string;
  avatar_url: string | null;
  role: 'USER' | 'PREMIUM' | 'ADMIN';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

/** Returned in the `data` field of login and refresh responses */
export interface BackendTokenData {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
  user: BackendUser;
}
