"""Service to call Open-Meteo for weather data."""
from typing import Dict
import requests


def get_current_weather(lat: float, lon: float) -> Dict[str, object]:
    """Return a small dict with current weather details.

    Uses Open-Meteo's `current_weather` endpoint.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto",
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if "current_weather" not in data:
        raise ValueError("weather_unavailable")

    cw = data["current_weather"]
    # current_weather contains temperature, windspeed, winddirection, weathercode, time
    return {
        "temperature": cw.get("temperature"),
        "windspeed": cw.get("windspeed"),
        "winddirection": cw.get("winddirection"),
        "weathercode": cw.get("weathercode"),
        "time": cw.get("time"),
    }
