import IPOListPage from '../../../components/IPOListPage';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Trending IPOs & Hot Market Opportunities',
  description: 'Track trending IPOs with high search queries, investor interest, grey market demand, and premium AI recommendations.',
};

export default function TrendingIPOs() {
  return (
    <IPOListPage 
      category="trending" 
      title="Trending IPOs" 
      description="Track high-interest deals based on community watchlists, search momentum, and Gray Market activity."
    />
  );
}
