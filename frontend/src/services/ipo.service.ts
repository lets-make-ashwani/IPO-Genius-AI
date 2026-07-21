/**
 * ipo.service.ts — Live FastAPI IPO Domain Service
 *
 * Connects Next.js frontend pages directly to live backend REST API endpoints
 * defined in API Contract V1 (`docs/api/API_CONTRACT_V1.md`).
 */

import { apiClient } from '../api/client';
import { toFrontendIPO } from '../lib/ipo.adapter';
import { IPO } from '../types';
import {
  BackendApiResponse,
  BackendIPOResponse,
  BackendIPOAnalysis,
  BackendIPOFinancials,
  BackendIPOSubscription,
  BackendIPODocuments,
  BackendIPONews,
} from '../types/api';

export const ipoService = {
  /**
   * Fetch paginated list of IPOs with filters and search
   */
  async getIPOs(
    search?: string,
    status?: string,
    sector?: string,
    exchange?: string,
    page: number = 1,
    limit: number = 20
  ): Promise<{ items: IPO[]; total: number }> {
    const params: Record<string, any> = {
      limit,
      offset: (page - 1) * limit,
    };

    if (search && search.trim()) {
      params.search = search.trim();
    }
    if (status && status !== 'All') {
      params.status = status.toUpperCase();
    }
    if (sector && sector !== 'All') {
      params.sector = sector.trim();
    }
    if (exchange && exchange !== 'All') {
      params.exchange = exchange.trim();
    }

    try {
      const response = await apiClient.get<BackendApiResponse<BackendIPOResponse[]>>('/ipos', { params });
      const rawItems = response.data || [];
      const items = rawItems.map(toFrontendIPO);
      
      const total = (response as any).pagination?.total || (response as any).meta?.total || items.length;
      return { items, total };
    } catch (error) {
      console.error('Error fetching IPOs:', error);
      return { items: [], total: 0 };
    }
  },

  /**
   * Fetch single IPO detail by ID or Slug
   */
  async getIPOById(idOrSlug: string): Promise<IPO | undefined> {
    try {
      const response = await apiClient.get<BackendApiResponse<BackendIPOResponse>>(`/ipos/${idOrSlug}`);
      if (!response.data) return undefined;
      return toFrontendIPO(response.data);
    } catch (error) {
      console.error(`Error fetching IPO ${idOrSlug}:`, error);
      return undefined;
    }
  },

  /**
   * Fetch Gemini AI Analysis for an IPO
   */
  async getIPOAnalysis(idOrSlug: string): Promise<BackendIPOAnalysis | undefined> {
    try {
      const response = await apiClient.get<BackendApiResponse<BackendIPOAnalysis>>(`/ipos/${idOrSlug}/analysis`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching AI analysis for ${idOrSlug}:`, error);
      return undefined;
    }
  },

  /**
   * Fetch Financials for an IPO
   */
  async getIPOFinancials(idOrSlug: string): Promise<BackendIPOFinancials | undefined> {
    try {
      const response = await apiClient.get<BackendApiResponse<BackendIPOFinancials>>(`/ipos/${idOrSlug}/financials`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching financials for ${idOrSlug}:`, error);
      return undefined;
    }
  },

  /**
   * Fetch Subscription Ratios for an IPO
   */
  async getIPOSubscription(idOrSlug: string): Promise<BackendIPOSubscription | undefined> {
    try {
      const response = await apiClient.get<BackendApiResponse<BackendIPOSubscription>>(`/ipos/${idOrSlug}/subscription`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching subscription for ${idOrSlug}:`, error);
      return undefined;
    }
  },

  /**
   * Fetch Regulatory Documents for an IPO
   */
  async getIPODocuments(idOrSlug: string): Promise<BackendIPODocuments | undefined> {
    try {
      const response = await apiClient.get<BackendApiResponse<BackendIPODocuments>>(`/ipos/${idOrSlug}/documents`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching documents for ${idOrSlug}:`, error);
      return undefined;
    }
  },

  /**
   * Fetch Related News Articles for an IPO
   */
  async getIPONews(idOrSlug: string): Promise<BackendIPONews | undefined> {
    try {
      const response = await apiClient.get<BackendApiResponse<BackendIPONews>>(`/ipos/${idOrSlug}/news`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching news for ${idOrSlug}:`, error);
      return undefined;
    }
  },

  /**
   * Fetch IPOs by dynamic categorization endpoint
   */
  async getIPOsByCategory(
    category: string,
    page: number = 1,
    limit: number = 20
  ): Promise<{ items: IPO[]; total: number }> {
    const params = {
      limit,
      offset: (page - 1) * limit,
    };
    try {
      const response = await apiClient.get<BackendApiResponse<BackendIPOResponse[]>>(`/ipos/${category}`, { params });
      const rawItems = response.data || [];
      const items = rawItems.map(toFrontendIPO);
      const total = (response as any).pagination?.total || (response as any).meta?.total || items.length;
      return { items, total };
    } catch (error) {
      console.error(`Error fetching IPOs for category ${category}:`, error);
      return { items: [], total: 0 };
    }
  },
};
