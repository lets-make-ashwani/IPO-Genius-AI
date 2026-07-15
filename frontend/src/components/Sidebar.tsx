'use client';

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
  AlertTriangle,
  FolderOpen
} from 'lucide-react';
import { authService } from '../services/auth.service';

interface SidebarProps {
  isAdmin?: boolean;
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

export default function Sidebar({ isAdmin = false }: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();

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
        { href: '/dashboard/watchlist', label: 'Watchlist', icon: Star, count: 3 },
        { href: '/dashboard/calendar', label: 'Calendar', icon: Calendar },
      ]
    },
    {
      title: 'ACCOUNT',
      items: [
        { href: '/dashboard/notifications', label: 'Notifications', icon: Bell, count: 5 },
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
        { href: '/admin/reports', label: 'Reports & Settings', icon: Layers },
      ]
    }
  ];

  const menuGroups = isAdmin ? adminMenu : userMenu;

  const handleLogout = async () => {
    await authService.logout();
    router.push('/login');
  };

  return (
    <aside className="w-70 fixed top-0 bottom-0 left-0 bg-sidebar-bg border-r border-border-subtle flex flex-col z-30">
      <div className="h-16 flex items-center gap-2 px-6 border-b border-border-subtle">
        <div className="p-1 rounded-md bg-gradient-to-tr from-primary-blue to-secondary-purple">
          <Sparkles className="w-4 h-4 text-white" />
        </div>
        <span className="font-bold text-lg text-white">IPO Genius AI</span>
        {isAdmin && (
          <span className="text-[10px] font-bold bg-amber-600 text-white px-1.5 py-0.5 rounded-sm">ADMIN</span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto py-6 px-4 space-y-8">
        {menuGroups.map((group) => (
          <div key={group.title} className="space-y-2">
            <h5 className="text-[10px] font-bold tracking-wider text-text-muted px-3">
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
                    className={`flex items-center justify-between px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-blue-600/10 text-primary-blue border-l-2 border-primary-blue'
                        : 'text-text-secondary hover:bg-card-bg hover:text-white'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <Icon className={`w-4 h-4 ${isActive ? 'text-primary-blue' : 'text-text-muted'}`} />
                      <span>{item.label}</span>
                    </div>
                    {item.badge && (
                      <span className={`text-[9px] font-bold text-white px-1.5 py-0.5 rounded-full ${item.badgeColor}`}>
                        {item.badge}
                      </span>
                    )}
                    {item.count && (
                      <span className="text-[10px] font-semibold bg-border-subtle text-white px-1.5 py-0.5 rounded-full">
                        {item.count}
                      </span>
                    )}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 border-t border-border-subtle">
        <div className="flex items-center justify-between p-3 rounded-lg bg-card-bg/60 border border-border-subtle">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-primary-blue/20 flex items-center justify-center font-bold text-primary-blue">
              RK
            </div>
            <div className="text-left">
              <h5 className="text-xs font-semibold text-white">Rahul Kumar</h5>
              <span className="text-[10px] font-medium text-accent-emerald bg-accent-emerald/10 px-1.5 py-0.2 rounded-sm">Pro Plan</span>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="p-1.5 rounded-md hover:bg-border-subtle text-text-muted hover:text-white transition-colors"
            title="Logout"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}
