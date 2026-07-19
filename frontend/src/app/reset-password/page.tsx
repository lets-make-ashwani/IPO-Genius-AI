'use client';

import { Suspense, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Sparkles, Lock, Star, ArrowLeft, Check, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { authService } from '../../services/auth.service';

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  const getPasswordStrength = () => {
    if (!password) return { label: 'Empty', color: 'bg-dark-bg', percent: 0 };
    if (password.length < 6) return { label: 'Weak', color: 'bg-red-500', percent: 25 };
    if (password.length < 10) return { label: 'Fair', color: 'bg-yellow-500', percent: 60 };
    return { label: 'Strong', color: 'bg-accent-emerald', percent: 100 };
  };

  const strength = getPasswordStrength();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!token) {
      setError('Password reset token is missing. Please request a new link.');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await authService.resetPassword(token, password);
      setIsSuccess(true);
    } catch (err: any) {
      setError(err.message || 'Failed to reset password. The link may have expired.');
    } finally {
      setLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="text-center py-6 space-y-6">
        <div className="w-16 h-16 rounded-full bg-accent-emerald/20 text-accent-emerald flex items-center justify-center mx-auto text-3xl shadow-lg shadow-accent-emerald/10 animate-pulse-glow">
          <Check className="w-8 h-8" />
        </div>
        
        <div className="space-y-2">
          <h2 className="text-2xl font-bold text-white">Password Reset Complete</h2>
          <p className="text-sm text-text-secondary leading-relaxed">
            Your password has been reset successfully. You can now log in using your new credentials.
          </p>
        </div>

        <div className="pt-4 border-t border-border-strong">
          <Link
            href="/login"
            className="w-full h-11 bg-primary-blue hover:bg-blue-700 text-white font-semibold text-sm rounded-md shadow-md transition-colors flex items-center justify-center"
          >
            Go to Sign In
          </Link>
        </div>
      </div>
    );
  }

  return (
    <>
      <Link href="/login" className="text-xs font-semibold text-text-muted hover:text-white flex items-center gap-1.5 mb-6">
        <ArrowLeft className="w-3.5 h-3.5" /> Back to Login
      </Link>
      
      <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-white mb-1.5">Reset Your Password</h2>
        <p className="text-xs text-text-muted">Enter a new secure password below to update your credentials.</p>
      </div>

      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-500 text-xs rounded-md flex items-start gap-2 mb-6">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Password */}
        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-text-muted uppercase tracking-wider">New Password</label>
          <div className="relative">
            <Lock className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
            <input
              required
              type={showPassword ? 'text' : 'password'}
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full h-10 pl-10 pr-10 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-3 text-text-muted hover:text-white"
            >
              {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>

          {/* Password Strength Indicator */}
          {password && (
            <div className="space-y-1.5 pt-1">
              <div className="flex justify-between text-[10px]">
                <span className="text-text-muted">Strength:</span>
                <span className="font-semibold text-white">{strength.label}</span>
              </div>
              <div className="h-1 w-full bg-border-strong rounded-full overflow-hidden">
                <div
                  className={`h-full transition-all duration-300 ${strength.color}`}
                  style={{ width: `${strength.percent}%` }}
                />
              </div>
            </div>
          )}
        </div>

        {/* Confirm Password */}
        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-text-muted uppercase tracking-wider">Confirm Password</label>
          <div className="relative">
            <Lock className="absolute left-3 top-3 w-4 h-4 text-text-muted" />
            <input
              required
              type="password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full h-10 pl-10 pr-4 rounded-md bg-dark-bg border border-border-subtle focus:border-primary-blue text-sm focus:outline-none focus:ring-1 focus:ring-primary-blue transition-all"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full h-11 rounded-md bg-primary-blue hover:bg-blue-700 text-white font-semibold text-sm shadow-md transition-colors flex items-center justify-center gap-2 disabled:opacity-55"
        >
          {loading ? 'Updating password...' : 'Reset Password'}
        </button>
      </form>
    </>
  );
}

export default function ResetPassword() {
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
          <Suspense fallback={<div className="text-center text-text-muted py-10">Loading reset parameters...</div>}>
            <ResetPasswordForm />
          </Suspense>
        </div>
      </div>
    </div>
  );
}
