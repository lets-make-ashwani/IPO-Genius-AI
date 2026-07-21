import IPOListPage from '../../../components/IPOListPage';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Most Subscribed IPOs & Bidding Demand',
  description: 'Track the most popular IPOs based on final retail, NII, QIB, and cumulative subscription times (multiples).',
};

export default function MostSubscribedIPOs() {
  return (
    <IPOListPage 
      category="most-subscribed" 
      title="Most Subscribed IPOs" 
      description="Track deals with the highest institutional, retail, and non-institutional investor subscription demand."
    />
  );
}
