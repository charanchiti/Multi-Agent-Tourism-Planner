"""Places child agent: gets coordinates via geocode tool and fetches nearby places."""
from typing import Dict, List
from langchain_core.tools import Tool
from tools.geocode_tool import geocode_tool
from tools.places_tool import places_tool


class PlacesAgent:
    """Agent to find nearby places for a given place string."""

    def __init__(self):
        self.geocode_tool: Tool = geocode_tool
        self.places_tool: Tool = places_tool

    def run(self, place: str) -> Dict[str, object]:
        try:
            lat, lon, disp = self.geocode_tool.func(place)
        except ValueError as e:
            if str(e) == "place_not_found":
                raise
            raise

        places = self.places_tool.func(lat, lon)
        # Keep a compact result
        summarized: List[Dict[str, object]] = []
        for p in places:
            summarized.append({"name": p.get("name"), "type": p.get("type"), "lat": p.get("lat"), "lon": p.get("lon")})

        return {"place": disp, "lat": lat, "lon": lon, "places": summarized}
