import IPOListPage from '../../../components/IPOListPage';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Live IPOs & Bidding Channels',
  description: 'Track all active and live IPOs currently open for bidding on BSE and NSE in India, with real-time grey market premiums (GMP) and subscription metrics.',
};

export default function LiveIPOs() {
  return (
    <IPOListPage 
      category="live" 
      title="Live IPOs" 
      description="Track active investment deals currently open for subscription, bidding, and allocation profiles in India."
    />
  );
}
