import Link from 'next/link';
import { Sparkles, MessageSquare } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-sidebar-bg border-t border-border-subtle py-12 px-6 md:px-12 text-text-muted">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <div className="p-1 rounded-md bg-gradient-to-tr from-primary-blue to-secondary-purple">
              <Sparkles className="w-4 h-4 text-white" />
            </div>
            <span className="text-white font-bold text-lg">IPO Genius AI</span>
          </div>
          <p className="text-sm">
            AI-powered platform making IPO research clear, simple, and accessible for retail investors.
          </p>
          <div className="flex gap-4 mt-2">
            <Link href="#" className="hover:text-white transition-colors" aria-label="Twitter">
              <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
              </svg>
            </Link>
            <Link href="#" className="hover:text-white transition-colors" aria-label="GitHub">
              <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.9-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0012 2z" />
              </svg>
            </Link>
            <Link href="#" className="hover:text-white transition-colors"><MessageSquare className="w-5 h-5" /></Link>
          </div>
        </div>

        <div>
          <h4 className="text-white font-semibold text-sm mb-4">Product</h4>
          <ul className="flex flex-col gap-2.5 text-sm">
            <li><Link href="/features" className="hover:text-white transition-colors">Features</Link></li>
            <li><Link href="/pricing" className="hover:text-white transition-colors">Pricing</Link></li>
            <li><Link href="/dashboard" className="hover:text-white transition-colors">AI Analysis</Link></li>
            <li><Link href="/faq" className="hover:text-white transition-colors">FAQ</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-semibold text-sm mb-4">Company</h4>
          <ul className="flex flex-col gap-2.5 text-sm">
            <li><Link href="/about" className="hover:text-white transition-colors">About Us</Link></li>
            <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
            <li><Link href="#" className="hover:text-white transition-colors">Careers</Link></li>
            <li><Link href="#" className="hover:text-white transition-colors">Press</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-white font-semibold text-sm mb-4">Legal</h4>
          <ul className="flex flex-col gap-2.5 text-sm">
            <li><Link href="/privacy-terms" className="hover:text-white transition-colors">Privacy Policy</Link></li>
            <li><Link href="/privacy-terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
            <li><Link href="#" className="hover:text-white transition-colors">Disclaimers</Link></li>
          </ul>
        </div>
      </div>

      <div className="max-w-7xl mx-auto border-t border-border-strong pt-6 flex flex-col md:flex-row items-center justify-between text-xs gap-4">
        <div>
          © {new Date().getFullYear()} IPO Genius AI. All rights reserved.
        </div>
        <div className="flex gap-6">
          <Link href="/privacy-terms" className="hover:text-white transition-colors">Privacy</Link>
          <Link href="/privacy-terms" className="hover:text-white transition-colors">Terms</Link>
          <Link href="#" className="hover:text-white transition-colors">Sitemap</Link>
        </div>
      </div>
    </footer>
  );
}
