"""LangChain Tool wrapper for geocoding service."""
from typing import Tuple
from langchain_core.tools import Tool
from services.geocode_service import geocode_place


def geocode(place: str) -> Tuple[float, float, str]:
    """Return (lat, lon, display_name) or raise ValueError("place_not_found")."""
    return geocode_place(place)


geocode_tool = Tool.from_function(func=geocode, name="geocode", description="Get latitude and longitude for a place using Nominatim (OpenStreetMap).")
