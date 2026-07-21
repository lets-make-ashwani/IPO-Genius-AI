'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
  LayoutDashboard,
  Calendar,
  Layers,
  Sparkles,
  MessageSquare,
  Star,
  Bell,
  CreditCard,
  User,
  Settings,
  LogOut,
  PlusCircle,
  Users,
  FolderOpen,
  X
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface SidebarProps {
  isAdmin?: boolean;
  isMobileOpen?: boolean;
  onMobileClose?: () => void;
}

interface MenuItem {
  href: string;
  label: string;
  icon: any;
  badge?: string;
  badgeColor?: string;
  count?: number;
}

interface MenuGroup {
  title: string;
  items: MenuItem[];
}

export default function Sidebar({ isAdmin = false, isMobileOpen = false, onMobileClose }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout } = useAuth();

  // Esc key listener & Body scroll lock
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isMobileOpen && onMobileClose) {
        onMobileClose();
      }
    };

    if (isMobileOpen) {
      document.body.style.overflow = 'hidden';
      window.addEventListener('keydown', handleKeyDown);
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isMobileOpen, onMobileClose]);

  const userMenu: MenuGroup[] = [
    {
      title: 'MAIN',
      items: [
        { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { href: '/dashboard/ipo', label: 'All IPOs', icon: FolderOpen },
      ]
    },
    {
      title: 'AI TOOLS',
      items: [
        { href: '/dashboard/chat', label: 'AI Chat', icon: MessageSquare, badge: 'NEW', badgeColor: 'bg-secondary-purple' },
        { href: '/dashboard/watchlist', label: 'Watchlist', icon: Star },
        { href: '/dashboard/calendar', label: 'Calendar', icon: Calendar },
      ]
    },
    {
      title: 'ACCOUNT',
      items: [
        { href: '/dashboard/notifications', label: 'Notifications', icon: Bell },
        { href: '/dashboard/subscription', label: 'Subscription', icon: CreditCard },
        { href: '/dashboard/profile', label: 'Profile', icon: User },
        { href: '/dashboard/settings', label: 'Settings', icon: Settings },
      ]
    }
  ];

  const adminMenu: MenuGroup[] = [
    {
      title: 'ADMIN MAIN',
      items: [
        { href: '/admin', label: 'Dashboard', icon: LayoutDashboard },
        { href: '/admin/ipo', label: 'IPO Management', icon: PlusCircle },
        { href: '/admin/users', label: 'Users & Billing', icon: Users },
      ]
    },
    {
      title: 'AI & ENGINE',
      items: [
        { href: '/admin/automation', label: 'Automation & AI', icon: Sparkles },
        { href: '/admin/reports', label: 'Reports & Engine', icon: Layers },
      ]
    }
  ];

  const menuGroups = isAdmin ? adminMenu : userMenu;

  const handleLogout = async () => {
    if (onMobileClose) onMobileClose();
    await logout();
    router.push('/login');
  };

  const handleLinkClick = () => {
    if (onMobileClose) onMobileClose();
  };

  const renderContent = () => (
    <div className="flex flex-col h-full bg-sidebar-bg">
      {/* Brand Header */}
      <div className="h-16 flex items-center justify-between px-6 border-b border-border-subtle shrink-0">
        <div className="flex items-center gap-2">
          <div className="p-1 rounded-md bg-gradient-to-tr from-primary-blue to-secondary-purple">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <span className="font-bold text-lg text-white">IPO Genius AI</span>
          {isAdmin && (
            <span className="text-[10px] font-bold bg-amber-600 text-white px-1.5 py-0.5 rounded-sm">ADMIN</span>
          )}
        </div>

        {/* Mobile Close Button */}
        {onMobileClose && (
          <button
            onClick={onMobileClose}
            className="md:hidden p-2 text-text-muted hover:text-white rounded-md min-w-[44px] min-h-[44px] flex items-center justify-center"
            aria-label="Close navigation drawer"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {/* Navigation Group Items */}
      <div className="flex-1 overflow-y-auto py-6 px-4 space-y-8">
        {menuGroups.map((group) => (
          <div key={group.title} className="space-y-2">
            <h5 className="text-[10px] font-bold tracking-wider text-text-muted px-3 uppercase">
              {group.title}
            </h5>
            <div className="space-y-1">
              {group.items.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href || (item.href !== '/dashboard' && item.href !== '/admin' && pathname.startsWith(item.href));
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={handleLinkClick}
                    className={`flex items-center justify-between px-3 py-2.5 rounded-md text-sm font-medium transition-colors min-h-[44px] ${
                      isActive
                        ? 'bg-blue-600/10 text-primary-blue border-l-2 border-primary-blue font-semibold'
                        : 'text-text-secondary hover:bg-card-bg hover:text-white'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-primary-blue' : 'text-text-muted'}`} />
                      <span>{item.label}</span>
                    </div>
                    {item.badge && (
                      <span className={`text-[9px] font-bold text-white px-1.5 py-0.5 rounded-full ${item.badgeColor}`}>
                        {item.badge}
                      </span>
                    )}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* User Footer Profile */}
      <div className="p-4 border-t border-border-subtle shrink-0">
        <div className="flex items-center justify-between p-3 rounded-lg bg-card-bg/60 border border-border-subtle">
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="w-9 h-9 rounded-full bg-primary-blue/20 flex items-center justify-center font-bold text-primary-blue shrink-0">
              {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
            </div>
            <div className="text-left truncate">
              <h5 className="text-xs font-semibold text-white truncate">{user?.name ?? 'User'}</h5>
              <span className="text-[10px] font-medium text-accent-emerald bg-accent-emerald/10 px-1.5 py-0.2 rounded-sm">
                {user?.role === 'ADMIN' ? 'Admin' : 'Pro'} Plan
              </span>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="p-2 rounded-md hover:bg-border-subtle text-text-muted hover:text-white transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center shrink-0"
            title="Logout"
            aria-label="Logout"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Fixed Sidebar */}
      <aside className="hidden md:flex w-64 lg:w-70 fixed top-0 bottom-0 left-0 bg-sidebar-bg border-r border-border-subtle flex-col z-30">
        {renderContent()}
      </aside>

      {/* Mobile Backdrop Overlay */}
      {isMobileOpen && (
        <div
          onClick={onMobileClose}
          className="fixed inset-0 bg-black/60 z-40 md:hidden backdrop-blur-sm transition-opacity"
          aria-hidden="true"
        />
      )}

      {/* Mobile Off-Canvas Slide-Out Drawer */}
      <aside
        className={`fixed inset-y-0 left-0 w-72 z-50 md:hidden shadow-2xl transition-transform duration-300 transform ${
          isMobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        aria-expanded={isMobileOpen}
        aria-label="Mobile Navigation Drawer"
      >
        {renderContent()}
      </aside>
    </>
  );
}
