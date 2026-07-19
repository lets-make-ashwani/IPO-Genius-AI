'use client';

interface FullScreenLoaderProps {
  message?: string;
}

/**
 * Full-screen loading overlay.
 * Used during session checks, token refreshes, and initial auth.
 * Prevents UI flickering while auth state is indeterminate.
 */
export default function FullScreenLoader({
  message = 'Loading...',
}: FullScreenLoaderProps) {
  return (
    <div className="min-h-screen bg-dark-bg flex flex-col items-center justify-center gap-5">
      {/* Spinner */}
      <div className="relative w-11 h-11">
        <div className="absolute inset-0 rounded-full border-2 border-primary-blue/20" />
        <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-primary-blue animate-spin" />
      </div>

      {/* Logo wordmark */}
      <div className="flex flex-col items-center gap-1">
        <span className="text-base font-bold text-white tracking-tight">
          IPO Genius AI
        </span>
        <span className="text-xs text-text-muted">{message}</span>
      </div>
    </div>
  );
}
