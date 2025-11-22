"""Local formatter for presenting weather and places results in natural language.

This module provides a small, deterministic formatter that creates a concise
human-readable summary from the structured results produced by the agents.
"""
from typing import Dict, Any, List


def _extract_weather_summary(raw_weather: Any) -> str:
    if not raw_weather:
        return "I don't have weather data for this location."

    # raw_weather may be the dict returned by WeatherAgent
    if isinstance(raw_weather, dict):
        place = raw_weather.get("place")
        w = raw_weather.get("weather") or {}
        time = w.get("time") if isinstance(w, dict) else None
        temp = w.get("temperature") if isinstance(w, dict) else None
        wind = w.get("windspeed") if isinstance(w, dict) else None

        parts: List[str] = []
        if place:
            parts.append(f"The location you asked about is {place}.")
        if time or temp is not None or wind is not None:
            weather_parts: List[str] = []
            if temp is not None:
                weather_parts.append(f"{temp}°C")
            if wind is not None:
                weather_parts.append(f"wind {wind} m/s")
            if weather_parts:
                parts.append(f"The current conditions are {' and '.join(weather_parts)}" + (f" (as of {time})." if time else "."))
        if not parts:
            return "I don't have detailed weather data for this location."

        return " ".join(parts)

    # fallback: raw string
    return f"Weather: {str(raw_weather)}"


def _extract_places_summary(raw_places: Any, max_items: int = 5) -> str:
    if not raw_places:
        return "I couldn't find notable places for this location."

    # raw_places may be a dict containing 'places' list or a list directly
    if isinstance(raw_places, dict):
        places_list = raw_places.get("places") or []
    else:
        places_list = raw_places if isinstance(raw_places, list) else []

    if not places_list:
        return "I couldn't find notable places for this location."

    # Build top-N list
    items = []
    for p in places_list[:max_items]:
        if isinstance(p, dict):
            name = p.get("name") or "unknown"
            kind = p.get("type") or "place"
            items.append(f"{name} ({kind})")
        else:
            items.append(str(p))

    if not items:
        return "I couldn't find notable places for this location."

    joined = ", ".join(items[:-1]) + (", and " + items[-1] if len(items) > 1 else items[0])
    return f"Top places to visit: {joined}."


def format_results(results: Dict[str, Any], want_weather: bool = True, want_places: bool = True) -> str:
    """Produce a human-friendly summary string from `results`.

    `results` is the dict returned by `ParentAgent.run`.
    """
    parts: List[str] = []

    # Weather
    if want_weather:
        raw_weather = results.get("weather")
        weather_text = _extract_weather_summary(raw_weather)
        parts.append(weather_text)

    # Places
    if want_places:
        raw_places = results.get("places")
        places_text = _extract_places_summary(raw_places)
        parts.append(places_text)

    if not parts:
        return "No information available for the given query."

    return "\n\n".join(parts)
