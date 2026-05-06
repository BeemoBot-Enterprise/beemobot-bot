# Last updated: 2026-05-06
"""Token bucket rate limiter for Riot API."""
import asyncio
import time


class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        """rate: tokens added per second; capacity: max tokens stored."""
        self.rate = rate
        self.capacity = capacity
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1):
        async with self._lock:
            while True:
                now = time.monotonic()
                elapsed = now - self.last_refill
                self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
                self.last_refill = now
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return
                wait = (tokens - self.tokens) / self.rate
                await asyncio.sleep(wait)


# Riot dev key allows ~50 req / 2 min => ~0.4 req/s. Be conservative at 0.3.
# Personal API key would be higher (we'll bump to 1.5 once granted).
RIOT_BUCKET = TokenBucket(rate=0.3, capacity=20)
