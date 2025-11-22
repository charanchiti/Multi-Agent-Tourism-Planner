"""Weather child agent: gets coordinates via geocode tool and fetches weather."""
from typing import Dict
from langchain_core.tools import Tool
from tools.geocode_tool import geocode_tool
from tools.weather_tool import weather_tool


class WeatherAgent:
    """Simple agent that uses tools to return weather for a place.

    This agent performs only deterministic calls to tools and returns structured results.
    """

    def __init__(self):
        self.geocode_tool: Tool = geocode_tool
        self.weather_tool: Tool = weather_tool

    def run(self, place: str) -> Dict[str, object]:
        # Geocode
        try:
            lat, lon, disp = self.geocode_tool.func(place)
        except ValueError as e:
            if str(e) == "place_not_found":
                raise
            raise

        # Get weather
        weather = self.weather_tool.func(lat, lon)
        return {"place": disp, "lat": lat, "lon": lon, "weather": weather}
