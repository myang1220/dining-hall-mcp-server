import httpx
import time
from typing import Any, Dict, List

BROWN_MENUS_URL = "https://esb-level1.brown.edu/services/oit/sys/brown-dining/v1/menus"


def fetch_menus(max_retries: int = 3, timeout_s: float = 15.0) -> List[Dict[str, Any]]:
    backoff = 0.5
    last_exc: Exception | None = None
    for _ in range(max_retries):
        try:
            with httpx.Client(timeout=timeout_s) as client:
                resp = client.get(BROWN_MENUS_URL, headers={"Accept": "application/json"})
                resp.raise_for_status()
                return resp.json()
        except Exception as exc:  # network or parsing error
            last_exc = exc
            time.sleep(backoff)
            backoff *= 2
    if last_exc:
        raise last_exc
    raise RuntimeError("Unknown error fetching menus")
