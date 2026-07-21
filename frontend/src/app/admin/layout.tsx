'use client';

import Sidebar from '../../components/Sidebar';
import Header from '../../components/Header';
import AuthGuard from '../../components/AuthGuard';
import { useState } from 'react';

export default function AdminLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [searchTerm, setSearchTerm] = useState('');
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  return (
    <AuthGuard requireAdmin>
      <div className="min-h-dvh bg-dark-bg text-text-primary flex relative max-w-full overflow-x-hidden">
        {/* Admin Sidebar — Fixed on desktop, Drawer on mobile */}
        <Sidebar 
          isAdmin={true} 
          isMobileOpen={isMobileOpen} 
          onMobileClose={() => setIsMobileOpen(false)} 
        />

        {/* Main Panel Content */}
        <div className="flex-1 flex flex-col w-full md:pl-64 lg:pl-70 min-h-dvh transition-all">
          {/* Sticky Admin Header */}
          <Header 
            onSearch={(term) => setSearchTerm(term)} 
            searchPlaceholder="Search admin database..."
            onToggleMobileMenu={() => setIsMobileOpen(true)}
          />
          
          <main className="flex-1 p-4 sm:p-6 md:p-8 space-y-6 max-w-full overflow-x-hidden">
            {children}
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}
