from __future__ import annotations
from typing import Any, Dict, List, Tuple, Optional


def index_by_date_location(raw_locations: List[Dict[str, Any]]) -> Dict[Tuple[str, str], List[Dict[str, Any]]]:
    """Build an index: (date, locationId) -> list of MealEntry dicts.
    Works directly on dicts to avoid strict schema coupling.
    """
    index: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for loc in raw_locations:
        location_id = loc.get("locationId")
        meals = loc.get("meals", {}) or {}
        for date_str, entries in meals.items():
            key = (date_str, location_id)
            index.setdefault(key, []).extend(entries or [])
    return index


def filter_index(
    index: Dict[Tuple[str, str], List[Dict[str, Any]]],
    date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    location_id: Optional[str] = None,
) -> Dict[Tuple[str, str], List[Dict[str, Any]]]:
    def in_range(d: str) -> bool:
        if date:
            return d == date
        if start_date and end_date:
            return start_date <= d <= end_date
        if start_date:
            return d >= start_date
        if end_date:
            return d <= end_date
        return True

    result: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for (d, loc), entries in index.items():
        if not in_range(d):
            continue
        if location_id and loc != location_id:
            continue
        result[(d, loc)] = entries
    return result
