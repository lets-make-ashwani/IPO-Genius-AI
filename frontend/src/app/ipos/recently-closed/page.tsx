import IPOListPage from '../../../components/IPOListPage';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Recently Closed IPOs & Allotment Status',
  description: 'View recently closed IPO subscriptions, final subscription multiples, grey market premiums, and links to check allotment status.',
};

export default function RecentlyClosedIPOs() {
  return (
    <IPOListPage 
      category="recently-closed" 
      title="Recently Closed IPOs" 
      description="Review final subscription demand metrics, allotment status links, and details for deals closed within the last 2 days."
    />
  );
}
