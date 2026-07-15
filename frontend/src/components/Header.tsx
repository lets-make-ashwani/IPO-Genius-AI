'use client';

import { useRouter, usePathname } from 'next/navigation';
import { Search, Bell, Sun, ChevronDown } from 'lucide-react';
import Link from 'next/link';

interface HeaderProps {
  onSearch?: (term: string) => void;
  searchPlaceholder?: string;
  showSearch?: boolean;
}

export default function Header({
  onSearch,
  searchPlaceholder = 'Search IPOs, sectors...',
  showSearch = true
}: HeaderProps) {
  const pathname = usePathname();
  const router = useRouter();

  // Create breadcrumbs from pathname
  const paths = pathname.split('/').filter(Boolean);
  const breadcrumbs = paths.map((path, idx) => {
    const href = '/' + paths.slice(0, idx + 1).join('/');
    const label = path.charAt(0).toUpperCase() + path.slice(1);
    return { href, label };
  });

  return (
    <header className="h-16 flex items-center justify-between px-8 border-b border-border-subtle bg-dark-bg z-20 sticky top-0">
      <div className="flex items-center gap-2 text-sm">
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

      {showSearch && onSearch && (
        <div className="relative w-96 hidden md:block">
          <Search className="absolute left-3.5 top-2.5 w-4 h-4 text-text-muted" />
          <input
            type="text"
            placeholder={searchPlaceholder}
            onChange={(e) => onSearch(e.target.value)}
            className="w-full h-9 pl-10 pr-4 rounded-md bg-card-bg/60 border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all"
          />
        </div>
      )}

      <div className="flex items-center gap-6">
        <button className="p-2 rounded-md hover:bg-card-bg text-text-muted hover:text-white transition-colors" title="Toggle theme">
          <Sun className="w-4 h-4" />
        </button>

        <div className="relative cursor-pointer">
          <button className="p-2 rounded-md hover:bg-card-bg text-text-muted hover:text-white transition-colors relative">
            <Bell className="w-4 h-4" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500" />
          </button>
        </div>

        <div className="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity">
          <div className="w-8 h-8 rounded-full bg-primary-blue/20 flex items-center justify-center font-bold text-primary-blue text-sm">
            RK
          </div>
          <ChevronDown className="w-4 h-4 text-text-muted" />
        </div>
      </div>
    </header>
  );
}
