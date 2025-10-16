from __future__ import annotations
from typing import List, Dict, Optional, Any, TypedDict
from pydantic import BaseModel


class MenuHours(BaseModel):
    start: str
    end: str


class MenuItem(BaseModel):
    itemId: int
    item: str
    icons: List[str] = []
    allergens: List[str] = []
    description: str | None = None
    itemType: str


class Station(BaseModel):
    stationId: int
    name: str
    items: List[MenuItem] = []


class Menu(BaseModel):
    date: str
    hours: MenuHours
    stations: List[Station]


class MealEntry(BaseModel):
    name: str
    meal: str
    menu: Menu


class Location(BaseModel):
    name: str
    locationId: str
    locationAddress: str | None = None
    meals: Dict[str, List[MealEntry]]  # date -> list of meal entries


# Normalized view
class NormalizedMeal(TypedDict):
    locationId: str
    locationName: str
    date: str
    meal: str
    stations: List[dict]
    hours: dict


class SummaryResult(TypedDict):
    text: str
    data: Dict[str, Any]
