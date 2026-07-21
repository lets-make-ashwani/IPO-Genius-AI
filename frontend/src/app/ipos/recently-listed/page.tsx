import IPOListPage from '../../../components/IPOListPage';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Recently Listed IPOs & Listing Day Gains',
  description: 'Analyze recent IPO listings on NSE and BSE, listing day price performance, GMP accuracy, and post-listing trading updates.',
};

export default function RecentlyListedIPOs() {
  return (
    <IPOListPage 
      category="recently-listed" 
      title="Recently Listed IPOs" 
      description="Inspect listing day performance, trading multiples, and market listings finalized within the last 2 days."
    />
  );
}
