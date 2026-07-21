'use client';

import { usePathname } from 'next/navigation';
import { Search, Bell, Sun, Menu } from 'lucide-react';
import Link from 'next/link';
import { useAuth } from '../context/AuthContext';

interface HeaderProps {
  onSearch?: (term: string) => void;
  searchPlaceholder?: string;
  showSearch?: boolean;
  onToggleMobileMenu?: () => void;
}

export default function Header({
  onSearch,
  searchPlaceholder = 'Search IPOs, sectors...',
  showSearch = true,
  onToggleMobileMenu
}: HeaderProps) {
  const pathname = usePathname();
  const { user } = useAuth();

  // Create breadcrumbs from pathname
  const paths = pathname.split('/').filter(Boolean);
  const breadcrumbs = paths.map((path, idx) => {
    const href = '/' + paths.slice(0, idx + 1).join('/');
    const label = path.charAt(0).toUpperCase() + path.slice(1);
    return { href, label };
  });

  return (
    <header className="h-16 flex items-center justify-between px-4 sm:px-6 md:px-8 border-b border-border-subtle bg-dark-bg/95 backdrop-blur-md z-20 sticky top-0 w-full">
      {/* Mobile Hamburger Menu + Brand Title / Desktop Breadcrumbs */}
      <div className="flex items-center gap-3">
        {onToggleMobileMenu && (
          <button
            onClick={onToggleMobileMenu}
            className="md:hidden p-2 text-text-muted hover:text-white rounded-md min-w-[44px] min-h-[44px] flex items-center justify-center -ml-2"
            aria-label="Open navigation menu"
          >
            <Menu className="w-5 h-5" />
          </button>
        )}

        {/* Mobile Brand Title */}
        <span className="md:hidden font-bold text-base text-white tracking-tight">
          IPO Genius AI
        </span>

        {/* Desktop Breadcrumbs */}
        <div className="hidden md:flex items-center gap-2 text-sm">
          <Link href="/dashboard" className="text-text-muted hover:text-white transition-colors">
            Home
          </Link>
          {breadcrumbs.map((crumb, idx) => (
            <span key={crumb.href} className="flex items-center gap-2">
              <span className="text-text-muted">/</span>
              <Link
                href={crumb.href}
                className={idx === breadcrumbs.length - 1 ? 'text-white font-medium' : 'text-text-muted hover:text-white transition-colors'}
              >
                {crumb.label}
              </Link>
            </span>
          ))}
        </div>
      </div>

      {/* Search Input on Desktop */}
      {showSearch && onSearch && (
        <div className="relative w-72 lg:w-96 hidden md:block">
          <Search className="absolute left-3.5 top-2.5 w-4 h-4 text-text-muted" />
          <input
            type="text"
            placeholder={searchPlaceholder}
            onChange={(e) => onSearch(e.target.value)}
            className="w-full h-9 pl-10 pr-4 rounded-md bg-card-bg/60 border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all text-white placeholder:text-text-muted"
          />
        </div>
      )}

      {/* Action Icons & Avatar */}
      <div className="flex items-center gap-2 sm:gap-4">
        <button className="p-2.5 rounded-md hover:bg-card-bg text-text-muted hover:text-white transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center" title="Toggle theme" aria-label="Toggle theme">
          <Sun className="w-4 h-4" />
        </button>

        <div className="relative">
          <button className="p-2.5 rounded-md hover:bg-card-bg text-text-muted hover:text-white transition-colors relative min-w-[44px] min-h-[44px] flex items-center justify-center" title="Notifications" aria-label="Notifications">
            <Bell className="w-4 h-4" />
            <span className="absolute top-2.5 right-2.5 w-2 h-2 rounded-full bg-red-500" />
          </button>
        </div>

        <Link href="/dashboard/profile" className="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity min-h-[44px]">
          <div className="w-8 h-8 rounded-full bg-primary-blue/20 flex items-center justify-center font-bold text-primary-blue text-sm">
            {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
          </div>
        </Link>
      </div>
    </header>
  );
}
