import IPOListPage from '../../../components/IPOListPage';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Top AI Rated IPOs & Analysis Reviews',
  description: 'Discover the highest-rated IPO investment opportunities based on our advanced Gemini AI scoring, SWOT profiles, and financial analysis.',
};

export default function TopRatedIPOs() {
  return (
    <IPOListPage 
      category="top-rated" 
      title="Top AI Rated IPOs" 
      description="Discover high-potential deals rated by our advanced Gemini AI analytics core based on prospectus scans and financial ratios."
    />
  );
}
