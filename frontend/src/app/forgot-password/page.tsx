'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Sparkles, Mail, Key, Star, ArrowLeft, Send, Check } from 'lucide-react';
import { authService } from '../../services/auth.service';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [isEmailSent, setIsEmailSent] = useState(false);
  const [countdown, setCountdown] = useState(45);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await authService.sendPasswordReset(email);
      setIsEmailSent(true);
      setCountdown(45);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isEmailSent && countdown > 0) {
      timer = setTimeout(() => setCountdown(prev => prev - 1), 1000);
    }
    return () => clearTimeout(timer);
  }, [isEmailSent, countdown]);

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
          
          {isEmailSent ? (
            <div className="text-center py-6 space-y-6">
              <div className="w-16 h-16 rounded-full bg-accent-emerald/20 text-accent-emerald flex items-center justify-center mx-auto text-3xl shadow-lg shadow-accent-emerald/10 animate-pulse-glow">
                <Check className="w-8 h-8" />
              </div>
              
              <div className="space-y-2">
                <h2 className="text-2xl font-bold text-white">Check your inbox</h2>
                <p className="text-sm text-text-secondary leading-relaxed">
                  We've sent a password reset link to <span className="font-semibold text-primary-blue">{email}</span>
                </p>
                <p className="text-xs text-text-muted leading-relaxed max-w-sm mx-auto">
                  The link will expire in 15 minutes. Check your spam folder if you don't see it.
                </p>
              </div>

              <div className="pt-4 border-t border-border-strong">
                <button className="w-full h-11 bg-primary-blue hover:bg-blue-700 text-white font-semibold text-sm rounded-md shadow-md transition-colors">
                  Open Email App
                </button>
                <span className="text-[11px] text-text-muted block mt-4 font-mono">
                  {countdown > 0 ? `Resend link available in 00:${countdown.toString().padStart(2, '0')}` : (
                    <button onClick={handleSubmit} className="text-primary-blue hover:underline font-semibold font-sans">
                      Resend Link Now
                    </button>
                  )}
                </span>
              </div>

              <Link href="/login" className="text-sm font-semibold text-text-muted hover:text-white flex items-center justify-center gap-1.5 pt-4">
                <ArrowLeft className="w-4 h-4" /> Back to Login
              </Link>
            </div>
          ) : (
            <>
              <Link href="/login" className="text-xs font-semibold text-text-muted hover:text-white flex items-center gap-1.5 mb-6">
                <ArrowLeft className="w-3.5 h-3.5" /> Back to Login
              </Link>
              
              <div className="text-center mb-8">
                <div className="p-2.5 rounded-full bg-primary-blue/10 w-fit mx-auto text-primary-blue mb-4">
                  <Key className="w-6 h-6" />
                </div>
                <h2 className="text-2xl font-bold text-white mb-1.5">Forgot your password?</h2>
                <p className="text-xs text-text-muted">Enter your email and we'll send you a reset link.</p>
              </div>

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

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full h-11 rounded-md bg-primary-blue hover:bg-blue-700 text-white font-semibold text-sm shadow-md transition-colors flex items-center justify-center gap-2 disabled:opacity-55"
                >
                  {loading ? 'Sending link...' : 'Send Reset Link →'}
                </button>
              </form>
            </>
          )}

        </div>
      </div>
    </div>
  );
}
