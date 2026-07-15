'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Sparkles } from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();

  const links = [
    { href: '/', label: 'Home' },
    { href: '/features', label: 'Features' },
    { href: '/pricing', label: 'Pricing' },
    { href: '/about', label: 'About' },
    { href: '/contact', label: 'Contact' },
    { href: '/faq', label: 'FAQ' },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass-panel h-16 flex items-center justify-between px-6 md:px-12 border-b border-border-subtle bg-dark-bg/80">
      <div className="flex items-center gap-2">
        <div className="p-1.5 rounded-lg bg-gradient-to-tr from-primary-blue to-secondary-purple">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
        <Link href="/" className="text-xl font-bold tracking-tight bg-gradient-to-r from-primary-blue to-secondary-purple bg-clip-text text-transparent">
          IPO Genius AI
        </Link>
      </div>

      <div className="hidden md:flex items-center gap-8">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={`text-sm font-medium transition-colors hover:text-white ${
              pathname === link.href ? 'text-white' : 'text-text-muted'
            }`}
          >
            {link.label}
          </Link>
        ))}
      </div>

      <div className="flex items-center gap-4">
        <Link href="/login" className="text-sm font-medium text-text-muted hover:text-white transition-colors">
          Login
        </Link>
        <Link
          href="/register"
          className="text-sm font-semibold bg-primary-blue hover:bg-blue-700 text-white px-4 py-2 rounded-md shadow-md transition-colors"
        >
          Get Started Free
        </Link>
      </div>
    </nav>
  );
}
