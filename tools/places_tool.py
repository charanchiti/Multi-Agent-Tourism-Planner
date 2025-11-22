"""LangChain Tool wrapper for places service."""
from typing import List, Dict
from langchain_core.tools import Tool
from services.places_service import find_places_near


def places_tool_func(lat: float, lon: float, radius: int = 2000, limit: int = 20) -> List[Dict[str, object]]:
    return find_places_near(lat, lon, radius=radius, limit=limit)


places_tool = Tool.from_function(func=places_tool_func, name="places", description="Find nearby tourism places using Overpass API.")
