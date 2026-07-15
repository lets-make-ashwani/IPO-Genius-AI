'use client';

import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';
import { useState } from 'react';

export default function AdminLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex">
      {/* Admin Sidebar */}
      <Sidebar isAdmin={true} />

      {/* Main Panel Content */}
      <div className="flex-1 flex flex-col pl-70 min-h-screen">
        {/* Sticky Admin Header */}
        <Header 
          onSearch={(term) => setSearchTerm(term)} 
          searchPlaceholder="Search admin database..."
        />
        
        <main className="flex-1 p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
