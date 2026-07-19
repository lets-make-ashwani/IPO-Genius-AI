export interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
  /** RBAC role from backend — separate from subscription plan */
  role: 'USER' | 'PREMIUM' | 'ADMIN';
  /** Billing subscription tier — wired in a future phase */
  plan: 'Free' | 'Pro' | 'Enterprise';
  status: 'Active' | 'Blocked';
  joinedDate: string;
}

export interface IPO {
  id: string;
  name: string;
  ticker: string;
  sector: string;
  status: 'Upcoming' | 'Open' | 'Closed' | 'Listed' | 'Draft';
  priceBand: { min: number; max: number };
  issueSize: number; // in Crores
  lotSize: number;
  openDate: string;
  closeDate: string;
  allotmentDate: string;
  refundDate: string;
  listingDate: string;
  aiScore: number;
  aiRecommendation: 'Strong Buy' | 'Buy' | 'Hold' | 'Avoid';
  gmp: number; // percentage premium
  overview: string;
  businessModel: string;
  financialSummary: {
    revenue: number[]; // last 3 years in Crores
    profit: number[]; // last 3 years in Crores
    ebitda: number[]; // last 3 years in Crores
    years: string[];
  };
  strengths: string[];
  risks: string[];
  swot: {
    strengths: string[];
    weaknesses: string[];
    opportunities: string[];
    threats: string[];
  };
}

export interface Transaction {
  id: string;
  userName: string;
  userEmail: string;
  amount: number;
  date: string;
  status: 'Success' | 'Failed' | 'Refunded';
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: string;
  aiScore?: number;
}
