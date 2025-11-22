"""Parent orchestrator agent: routes queries to child agents based on parsed intent."""
from typing import Dict
from agents.weather_agent import WeatherAgent
from agents.places_agent import PlacesAgent


class ParentAgent:
    """Orchestrates WeatherAgent and PlacesAgent.

    The parent agent decides which child agents to invoke and combines results.
    """

    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()

    def run(self, place: str, want_weather: bool = True, want_places: bool = True) -> Dict[str, object]:
        if not place or not place.strip():
            raise ValueError("Empty place")

        results: Dict[str, object] = {"input_place": place}

        # Attempt geocoding via the child agents; each child will raise ValueError("place_not_found") if not found
        if want_weather:
            try:
                results["weather"] = self.weather_agent.run(place)
            except ValueError as e:
                if str(e) == "place_not_found":
                    results["weather_error"] = "I don’t think this place exists."
                else:
                    results["weather_error"] = str(e)

        if want_places:
            try:
                results["places"] = self.places_agent.run(place)
            except ValueError as e:
                if str(e) == "place_not_found":
                    results["places_error"] = "I don’t think this place exists."
                else:
                    results["places_error"] = str(e)

        return results
