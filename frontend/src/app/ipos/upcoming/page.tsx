import IPOListPage from '../../../components/IPOListPage';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Upcoming IPOs Calendar & Schedules',
  description: 'View the complete pipeline of upcoming IPOs, draft red herring prospectuses (DRHP) filed with SEBI, and expected listing timelines.',
};

export default function UpcomingIPOs() {
  return (
    <IPOListPage 
      category="upcoming" 
      title="Upcoming IPOs" 
      description="Preview upcoming IPO listings, timelines, draft SEBI prospectuses, and price bands before bidding opens."
    />
  );
}
