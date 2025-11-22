"""Simple query parser to decide which agents to run.

This parser inspects the user's free-text input and determines whether the user
is asking for weather, places, or both. It also extracts a likely place name.
"""
from typing import Dict


def parse_query(query: str) -> Dict[str, object]:
    """Return a dict with keys: place (str), want_weather (bool), want_places (bool).

    The parser uses simple keyword checks; it's intentionally small and deterministic.
    """
    q = (query or "").strip()
    q_lower = q.lower()

    weather_keywords = ["weather", "temperature", "forecast", "rain", "snow", "sunny"]
    places_keywords = ["place", "places", "attraction", "attractions", "tourist", "things to do", "restaurant", "cafe", "museum"]

    want_weather = any(k in q_lower for k in weather_keywords)
    want_places = any(k in q_lower for k in places_keywords)

    # If neither explicitly requested, assume user wants both information types
    if not (want_weather or want_places):
        want_weather = True
        want_places = True

    # Heuristic to extract a place: look for "in <place>" or take the last token group
    place = ""
    if " in " in q_lower:
        # split on ' in ' and take last part
        place = q_lower.split(" in ")[-1].strip()
    else:
        # fallback: use the whole query if short, else take last 3 words
        tokens = q.split()
        if len(tokens) <= 4:
            place = q
        else:
            place = " ".join(tokens[-4:])

    return {"place": place, "want_weather": want_weather, "want_places": want_places}
