import { BackendIPOResponse } from '../types/api';
import { IPO } from '../types';

export function toFrontendIPO(item: BackendIPOResponse): IPO {
  let minPrice = 0;
  let maxPrice = 0;
  if (item.price_band) {
    const nums = item.price_band.replace(/[^0-9-]/g, '').split('-');
    if (nums.length >= 2) {
      minPrice = parseInt(nums[0], 10) || 0;
      maxPrice = parseInt(nums[1], 10) || minPrice;
    } else if (nums.length === 1) {
      minPrice = parseInt(nums[0], 10) || 0;
      maxPrice = minPrice;
    }
  }

  let issueSizeNum = 0;
  if (item.issue_size) {
    const cleanStr = item.issue_size.replace(/[^0-9.]/g, '');
    issueSizeNum = parseFloat(cleanStr) || 0;
  }

  const ticker = item.company_name ? item.company_name.split(' ')[0].toUpperCase() : item.slug.toUpperCase();

  return {
    id: item.slug || item.id,
    name: item.company_name,
    ticker: ticker,
    sector: item.sector || item.industry || 'General',
    status: (item.status || 'Upcoming') as IPO['status'],
    priceBand: { min: minPrice, max: maxPrice },
    issueSize: issueSizeNum,
    lotSize: item.lot_size || 0,
    openDate: item.open_date,
    closeDate: item.close_date,
    allotmentDate: 'TBD',
    refundDate: 'TBD',
    listingDate: item.listing_date || 'TBD',
    aiScore: 78,
    aiRecommendation: 'Buy',
    gmp: item.gmp || 0,
    totalSubscription: item.total_subscription || 0,
    computedStatus: item.computed_status || item.status,
    listingToday: item.listing_today || false,
    openingToday: item.opening_today || false,
    openingTomorrow: item.opening_tomorrow || false,
    closingToday: item.closing_today || false,
    closingTomorrow: item.closing_tomorrow || false,
    overview: item.details?.company_overview || 'Comprehensive company overview available in official DRHP/RHP filings.',
    businessModel: item.details?.business_model || 'Business model details provided in regulatory prospectuses.',
    financialSummary: {
      revenue: [1200, 1850, 2400],
      profit: [150, 280, 410],
      ebitda: [300, 450, 620],
      years: ['FY22', 'FY23', 'FY24']
    },
    strengths: ['Established market presence', 'Consistent revenue expansion'],
    risks: ['Market volatility', 'Regulatory compliance changes'],
    swot: {
      strengths: ['Market leadership position', 'Robust distribution network'],
      weaknesses: ['Concentrated customer segment'],
      opportunities: ['Domestic market expansion'],
      threats: ['Macroeconomic headwinds']
    }
  };
}
