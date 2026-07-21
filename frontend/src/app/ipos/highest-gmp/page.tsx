import IPOListPage from '../../../components/IPOListPage';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Highest GMP IPOs & Grey Market Premium Index',
  description: 'View active IPOs ranked by grey market premium (GMP), expected listing gains, and premium percentage rates.',
};

export default function HighestGMPIPOs() {
  return (
    <IPOListPage 
      category="highest-gmp" 
      title="Highest GMP IPOs" 
      description="View deals sorted by grey market premiums (GMP) and listing day premium forecasts."
    />
  );
}
