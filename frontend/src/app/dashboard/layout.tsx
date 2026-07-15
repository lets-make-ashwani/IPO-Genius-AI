'use client';

import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';
import { useState } from 'react';

export default function DashboardLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex">
      {/* Sidebar - fixed */}
      <Sidebar isAdmin={false} />

      {/* Main Content Space */}
      <div className="flex-1 flex flex-col pl-70 min-h-screen">
        {/* Header - sticky */}
        <Header 
          onSearch={(term) => setSearchTerm(term)} 
          searchPlaceholder="Search listings, sectors..."
        />
        
        {/* Children content */}
        <main className="flex-1 p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
