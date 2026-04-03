import time
import functools
from threading import Lock

class TokenBucket:
    def __init__(self, rate: float, capacity: float):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = Lock()

    def consume(self, tokens: float = 1.0) -> bool:
        with self.lock:
            now = time.time()
            elapsed = now - self.last_update
            self.last_update = now
            
            # Refill tokens
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

# Global limiters
_limiters = {
    "yfinance": TokenBucket(rate=10/60, capacity=10),  # 10 req/min
    "default": TokenBucket(rate=20/60, capacity=20)
}

def rate_limited(service_name: str = "default"):
    """
    Decorator to rate limit function calls using a Token Bucket algorithm.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            limiter = _limiters.get(service_name, _limiters["default"])
            
            # Wait for token
            while not limiter.consume():
                time.sleep(0.1)
                
            return func(*args, **kwargs)
        return wrapper
    return decorator

def with_retry(max_retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_retries - 1: raise e
                    time.sleep(delay * (2 ** i)) # Exponential backoff
        return wrapper
    return decorator