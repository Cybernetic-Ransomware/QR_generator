import threading
import time
import uuid


class ResultStore:
    """Thread-safe in-memory store for generated QR payloads, keyed by token.

    Each entry has a TTL; entries beyond max_entries are evicted FIFO.
    """

    def __init__(self, ttl: int = 600, max_entries: int = 128) -> None:
        self._ttl = ttl
        self._max_entries = max_entries
        self._store: dict[str, tuple[float, dict]] = {}
        self._lock = threading.Lock()

    def put(self, payload: dict) -> str:
        """Store payload and return the generated token."""
        token = uuid.uuid4().hex
        with self._lock:
            self._evict()
            self._store[token] = (time.monotonic(), payload)
        return token

    def get(self, token: str) -> dict | None:
        """Return payload for token, or None if missing or expired."""
        with self._lock:
            entry = self._store.get(token)
            if entry is None:
                return None
            timestamp, payload = entry
            if time.monotonic() - timestamp > self._ttl:
                del self._store[token]
                return None
            return payload

    def _evict(self) -> None:
        """Remove expired entries; if still over cap, drop oldest."""
        now = time.monotonic()
        expired = [k for k, (ts, _) in self._store.items() if now - ts > self._ttl]
        for k in expired:
            del self._store[k]
        while len(self._store) >= self._max_entries:
            oldest = next(iter(self._store))
            del self._store[oldest]
