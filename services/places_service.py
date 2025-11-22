"""Service to call Overpass API to find nearby places/tourism POIs."""
from typing import List, Dict
import requests


def find_places_near(lat: float, lon: float, radius: int = 2000, limit: int = 20) -> List[Dict[str, object]]:
    """Query Overpass API and return a list of places with name and type.

    Returns an empty list if nothing found.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"

    # A compact Overpass QL query that looks for tourism nodes/ways/relations and common amenities
    query = f"""
[out:json][timeout:25];
(
  node["tourism"](around:{radius},{lat},{lon});
  way["tourism"](around:{radius},{lat},{lon});
  relation["tourism"](around:{radius},{lat},{lon});
  node["amenity"~"restaurant|cafe|bar|pub"](around:{radius},{lat},{lon});
);
out center {limit};
"""

    resp = requests.post(overpass_url, data={"data": query}, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    results: List[Dict[str, object]] = []
    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name")
        if not name:
            continue
        kind = tags.get("tourism") or tags.get("amenity") or "unknown"

        # For ways/relations Overpass returns a 'center' with lat/lon
        if el.get("type") == "node":
            plat = el.get("lat")
            plon = el.get("lon")
        else:
            center = el.get("center", {})
            plat = center.get("lat")
            plon = center.get("lon")

        results.append({"name": name, "type": kind, "lat": plat, "lon": plon})

    return results[:limit]
