'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Sparkles, Mail, Lock, Eye, EyeOff, Star, AlertCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function Login() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const user = await login(email, password);
      // Route based on backend role — never infer from email address
      if (user.role === 'ADMIN') {
        router.push('/admin');
      } else {
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.message || 'Something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-bg text-text-primary flex flex-col md:flex-row">
      
      {/* Left Brand Panel */}
      <div className="w-full md:w-[42%] bg-gradient-to-tr from-dark-bg to-[#1e0a3c] border-r border-border-subtle flex flex-col justify-between p-12 relative overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-secondary-purple/10 rounded-full blur-[80px] pointer-events-none" />
        
        {/* Logo */}
        <div className="flex items-center gap-2">
          <div className="p-1 rounded-md bg-gradient-to-tr from-primary-blue to-secondary-purple">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <span className="font-bold text-lg text-white">IPO Genius AI</span>
        </div>

        {/* Testimonial */}
        <div className="space-y-6 max-w-sm">
          <p className="text-lg italic text-text-secondary leading-relaxed">
            "IPO Genius AI helped me analyze over 50 IPOs and make confident investment decisions."
          </p>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-primary-blue/20 flex items-center justify-center font-bold text-primary-blue">
              RK
            </div>
            <div>
              <h5 className="text-sm font-semibold text-white">Rahul Kumar</h5>
              <span className="text-xs text-text-muted">Retail Investor, Mumbai</span>
            </div>
          </div>
          <div className="flex gap-1">
            {[...Array(5)].map((_, i) => (
              <Star key={i} className="w-4 h-4 text-yellow-500 fill-yellow-500" />
            ))}
          </div>
        </div>

        {/* Trust Stats */}
        <div className="flex gap-4">
          <div className="px-3 py-1.5 rounded-full bg-card-bg/60 border border-border-subtle/50 text-[10px] text-text-muted flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-primary-blue" />
            10,000+ Investors
          </div>
          <div className="px-3 py-1.5 rounded-full bg-card-bg/60 border border-border-subtle/50 text-[10px] text-text-muted flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-secondary-purple" />
            500+ IPOs Analyzed
          </div>
        </div>
      </div>

      {/* Right Form Panel */}
      <div className="flex-1 flex items-center justify-center bg-dark-bg p-6">
        <div className="w-full max-w-[460px] bg-card-bg border border-border-strong rounded-lg p-8 shadow-2xl relative">
          
          <div className="text-center mb-8">
            <div className="p-2.5 rounded-full bg-primary-blue/10 w-fit mx-auto text-primary-blue mb-4">
              <Sparkles className="w-6 h-6" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-1.5">Welcome back</h2>
            <p className="text-xs text-text-muted">Sign in to your IPO Genius AI account</p>
          </div>

          {error && (
            <div className="p-3 mb-6 bg-red-500/10 border border-red-500/20 text-red-400 rounded-md text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-1.5">
              <label className="text-[10px] font-bold text-text-muted uppercase tracking-wider">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
                <input
                  required
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full h-10 pl-10 pr-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between items-center">
                <label className="text-[10px] font-bold text-text-muted uppercase tracking-wider">Password</label>
                <Link href="/forgot-password" className="text-xs font-semibold text-primary-blue hover:underline">
                  Forgot password?
                </Link>
              </div>
              <div className="relative">
                <Lock className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
                <input
                  required
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full h-10 pl-10 pr-10 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(prev => !prev)}
                  className="absolute right-3 top-3 text-text-muted hover:text-white"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="remember"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="w-4 h-4 rounded border-border-subtle bg-dark-bg text-primary-blue focus:ring-primary-blue"
              />
              <label htmlFor="remember" className="text-xs font-semibold text-text-secondary cursor-pointer">
                Remember me for 30 days
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full h-11 rounded-md bg-primary-blue hover:bg-blue-700 text-white font-semibold text-sm shadow-md transition-colors flex items-center justify-center gap-2 disabled:opacity-55"
            >
              {loading ? 'Signing in...' : 'Sign in to your account →'}
            </button>
          </form>

          <div className="relative my-6 text-center">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-border-strong" /></div>
            <span className="relative bg-card-bg px-3 text-xs text-text-muted">or continue with</span>
          </div>

          <button className="w-full h-10 rounded-md border border-border-subtle bg-dark-bg hover:bg-card-bg transition-colors flex items-center justify-center gap-2 text-sm font-semibold text-white">
            <span className="w-4 h-4 rounded-full bg-white text-black font-extrabold text-[10px] flex items-center justify-center">G</span>
            Continue with Google
          </button>

          <div className="mt-8 text-center text-xs text-text-muted">
            Don't have an account?{' '}
            <Link href="/register" className="font-semibold text-primary-blue hover:underline">
              Create one →
            </Link>
          </div>

        </div>
      </div>
    </div>
  );
}
