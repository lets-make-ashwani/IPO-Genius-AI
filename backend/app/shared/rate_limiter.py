from fastapi import Request, status
import time
from collections import defaultdict
import threading
from app.shared.exceptions import AppException

class InMemoryRateLimiter:
    """
    Thread-safe in-memory rate limiter using a sliding window.
    Designed to protect sensitive auth endpoints like forgot-password and reset-password.
    """
    def __init__(self, requests_limit: int, window_seconds: int):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        # Maps key (IP or email) -> list of timestamps
        self.history = defaultdict(list)
        self.lock = threading.Lock()

    def check_rate_limit(self, key: str):
        with self.lock:
            now = time.time()
            # Filter out timestamps older than the sliding window
            self.history[key] = [t for t in self.history[key] if now - t < self.window_seconds]
            
            if len(self.history[key]) >= self.requests_limit:
                # Calculate retry-after wait time
                wait_time = int(self.window_seconds - (now - self.history[key][0]))
                raise AppException(
                    message=f"Too many password reset attempts. Please try again in {wait_time} seconds.",
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS
                )
            
            # Record the current request timestamp
            self.history[key].append(now)

# Limit to 5 attempts per 15 minutes (900 seconds)
forgot_password_limiter = InMemoryRateLimiter(requests_limit=5, window_seconds=900)
# Limit to 5 attempts per 15 minutes (900 seconds)
reset_password_limiter = InMemoryRateLimiter(requests_limit=5, window_seconds=900)
