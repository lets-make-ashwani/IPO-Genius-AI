'use client';

import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';
import AuthGuard from '../../components/AuthGuard';
import { useState } from 'react';

export default function DashboardLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [searchTerm, setSearchTerm] = useState('');
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  return (
    <AuthGuard>
      <div className="min-h-dvh bg-dark-bg text-text-primary flex relative max-w-full overflow-x-hidden">
        {/* Sidebar — Fixed on desktop, Drawer on mobile */}
        <Sidebar 
          isAdmin={false} 
          isMobileOpen={isMobileOpen} 
          onMobileClose={() => setIsMobileOpen(false)} 
        />

        {/* Main Content Space */}
        <div className="flex-1 flex flex-col w-full md:pl-64 lg:pl-70 min-h-dvh transition-all">
          {/* Header — Sticky Top */}
          <Header 
            onSearch={(term) => setSearchTerm(term)} 
            searchPlaceholder="Search listings, sectors..."
            onToggleMobileMenu={() => setIsMobileOpen(true)}
          />
          
          {/* Children content */}
          <main className="flex-1 p-4 sm:p-6 md:p-8 space-y-6 max-w-full overflow-x-hidden">
            {children}
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}
