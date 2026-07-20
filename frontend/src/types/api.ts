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

/** Backend IPOResponse from FastAPI */
export interface BackendIPOResponse {
  id: string;
  company_name: string;
  slug: string;
  logo_url: string | null;
  sector: string | null;
  industry: string | null;
  exchange: 'NSE' | 'BSE' | 'BOTH';
  ipo_type: 'MAINBOARD' | 'SME';
  price_band: string;
  lot_size: number;
  issue_size: string;
  open_date: string;
  close_date: string;
  listing_date: string | null;
  status: 'Upcoming' | 'Open' | 'Closed' | 'Listed';
  gmp: number | null;
  gmp_last_updated: string | null;
  drhp_url: string | null;
  rhp_url: string | null;
  prospectus_url: string | null;
  source: string | null;
  source_url: string | null;
  last_synced_at: string | null;
  is_verified: boolean;
  details?: {
    company_overview?: string | null;
    business_model?: string | null;
    promoters?: string | null;
    objectives?: string | null;
    financial_summary?: string | null;
  } | null;
  created_at: string;
  updated_at: string;
}

export interface BackendIPOAnalysis {
  ipo_id: string;
  overall_score: number;
  financial_score: number | null;
  management_score: number | null;
  valuation_score: number | null;
  risk_score: number | null;
  recommendation: string;
  summary: string | null;
  strengths: string[];
  weaknesses: string[];
  risks: string[];
  model_provider: string | null;
  model_version: string | null;
}

export interface BackendIPOFinancials {
  ipo_id: string;
  financial_summary: string | null;
  revenue_growth: string | null;
  ebitda_margin: string | null;
  pat_margin: string | null;
}

export interface BackendIPOSubscription {
  ipo_id: string;
  qib_subscription: number;
  nii_subscription: number;
  retail_subscription: number;
  employee_subscription: number;
  total_subscription: number;
  last_updated_at: string | null;
}

export interface BackendIPODocuments {
  ipo_id: string;
  drhp_url: string | null;
  rhp_url: string | null;
  prospectus_url: string | null;
}

export interface BackendIPONews {
  ipo_id: string;
  articles: Array<{
    title: string;
    source: string;
    url: string;
    published_at: string;
    sentiment: string;
  }>;
}

