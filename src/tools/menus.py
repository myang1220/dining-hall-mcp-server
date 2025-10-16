from __future__ import annotations
from typing import Any, Dict, Optional

from src.cache.cache import get_cache
from src.clients.dining_api_client import fetch_menus
from src.domain.normalize import index_by_date_location, filter_index
from src.domain.summarize import summarize_entries, render_text


_def_top_n = 5


def _get_payload() -> list[dict[str, Any]]:
    cache = get_cache()
    payload = cache.get()
    if payload is not None:
        return payload
    payload = fetch_menus()
    cache.set(payload)
    return payload


def get_menus_tool(
    *,
    date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    location_id: Optional[str] = None,
) -> Dict[str, Any]:
    payload = _get_payload()
    idx = index_by_date_location(payload)
    filtered = filter_index(idx, date=date, start_date=start_date, end_date=end_date, location_id=location_id)

    # Return a compact normalized shape
    out: dict[str, Any] = {}
    for (d, loc), entries in filtered.items():
        out.setdefault(d, {})[loc] = entries
    return {"data": out}


def summarize_menus_tool(
    *,
    date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    location_id: Optional[str] = None,
    top_n: int = _def_top_n,
) -> Dict[str, Any]:
    payload = _get_payload()
    idx = index_by_date_location(payload)
    filtered = filter_index(idx, date=date, start_date=start_date, end_date=end_date, location_id=location_id)

    summaries: list[dict[str, Any]] = []
    texts: list[str] = []

    # Build location name lookup
    loc_name: dict[str, str] = {loc.get("locationId"): loc.get("name") for loc in payload}

    for (d, loc), entries in sorted(filtered.items()):
        by_meal: dict[str, list[dict[str, Any]]] = {}
        for e in entries:
            meal = e.get("meal") or ""
            by_meal.setdefault(meal, []).append(e)
        for meal, es in by_meal.items():
            s = summarize_entries(es, top_n=top_n)
            summaries.append({
                "date": d,
                "locationId": loc,
                "locationName": loc_name.get(loc, loc),
                "meal": meal,
                **s,
            })
            texts.append(
                render_text(loc_name.get(loc, loc), meal, s)
            )

    return {"text": "\n\n".join(texts), "data": {"summaries": summaries}}


def refresh_cache_tool(
    *, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> Dict[str, Any]:
    # Currently ignores date window since API returns multi-day; kept for future
    payload = fetch_menus()
    get_cache().set(payload)
    return {"text": "Cache refreshed", "data": {"count": len(payload)}}
