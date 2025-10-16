from __future__ import annotations
from typing import Any, Dict, List, Tuple


ICON_MAP = {
    "VGN": "vegan",
    "VGTN": "vegetarian",
    "HL": "halal",
}


def _is_highlight(item: Dict[str, Any]) -> bool:
    if item.get("itemType") != "recipe":
        return False
    name = (item.get("item") or "").lower()
    if any(word in name for word in ["sauce", "dressing", "condiment"]):
        return False
    return True


def summarize_entries(entries: List[Dict[str, Any]], top_n: int = 5) -> Dict[str, Any]:
    highlights: List[str] = []
    dietary_counts: Dict[str, int] = {}
    allergens: Dict[str, int] = {}
    stations_out: List[Dict[str, Any]] = []

    hours_start = None
    hours_end = None

    for entry in entries:
        menu = entry.get("menu", {})
        hours = menu.get("hours", {}) or {}
        if hours:
            hours_start = hours.get("start", hours_start)
            hours_end = hours.get("end", hours_end)
        for st in menu.get("stations", []) or []:
            station_name = st.get("name")
            items_out: List[str] = []
            for it in st.get("items", []) or []:
                # dietary
                for icon in it.get("icons", []) or []:
                    label = ICON_MAP.get(icon, icon)
                    dietary_counts[label] = dietary_counts.get(label, 0) + 1
                for alg in it.get("allergens", []) or []:
                    allergens[alg] = allergens.get(alg, 0) + 1
                if _is_highlight(it) and len(highlights) < top_n:
                    highlights.append(it.get("item", ""))
                items_out.append(it.get("item", ""))
            stations_out.append({
                "name": station_name,
                "items": items_out,
            })

    return {
        "hours": {"start": hours_start, "end": hours_end},
        "stations": stations_out,
        "highlights": highlights,
        "dietary_counts": dietary_counts,
        "allergen_counts": allergens,
    }


def render_text(location_name: str, meal: str, summary: Dict[str, Any]) -> str:
    parts: List[str] = []
    hours = summary.get("hours") or {}
    if hours.get("start") and hours.get("end"):
        parts.append(f"{meal} at {location_name} ({hours['start']} – {hours['end']}):")
    else:
        parts.append(f"{meal} at {location_name}:")

    highs = summary.get("highlights", [])
    if highs:
        parts.append("Highlights: " + ", ".join(highs))

    return "\n".join(parts)
