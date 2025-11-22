"""LangChain Tool wrapper for weather service."""
from typing import Dict
from langchain_core.tools import Tool
from services.weather_service import get_current_weather


def weather_tool_func(lat: float, lon: float) -> Dict[str, object]:
    return get_current_weather(lat, lon)


weather_tool = Tool.from_function(func=weather_tool_func, name="weather", description="Get current weather for given latitude and longitude using Open-Meteo.")
