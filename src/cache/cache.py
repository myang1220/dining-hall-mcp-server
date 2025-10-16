import json
import os
import time
from typing import Any, Dict, List, Optional

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".cache")
DEFAULT_TTL_S = 4 * 60 * 60  # 4 hours


class MenuCache:
    def __init__(self, ttl_s: int = DEFAULT_TTL_S) -> None:
        self.ttl_s = ttl_s
        self._data: Optional[List[Dict[str, Any]]] = None
        self._fetched_at: Optional[float] = None
        os.makedirs(CACHE_DIR, exist_ok=True)
        self._disk_path = os.path.join(CACHE_DIR, "menus-window.json")

    def get(self) -> Optional[List[Dict[str, Any]]]:
        if self._data is not None and self._fetched_at is not None:
            if (time.time() - self._fetched_at) < self.ttl_s:
                return self._data
        # try disk
        if os.path.exists(self._disk_path):
            try:
                with open(self._disk_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                # do not update in-memory fetched_at; treat as last-good but stale
                return payload
            except Exception:
                return None
        return None

    def set(self, payload: List[Dict[str, Any]]) -> None:
        self._data = payload
        self._fetched_at = time.time()
        # write to disk best-effort
        try:
            with open(self._disk_path, "w", encoding="utf-8") as f:
                json.dump(payload, f)
        except Exception:
            pass


_global_cache = MenuCache()


def get_cache() -> MenuCache:
    return _global_cache
