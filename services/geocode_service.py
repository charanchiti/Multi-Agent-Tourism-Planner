"""Service to call Nominatim (OpenStreetMap) for geocoding.
"""
from typing import Tuple
import os
import time
import requests


def geocode_place(place: str) -> Tuple[float, float, str]:
    """Return (latitude, longitude, display_name) for a place.

    Uses Nominatim (OpenStreetMap). To comply with Nominatim usage policy,
    set the environment variable `NOMINATIM_EMAIL` to a contact email address
    which will be sent with requests. This helps avoid 403/blocked responses.

    Raises ValueError("place_not_found") if the place isn't found.
    Raises RuntimeError for API errors like 403 Forbidden.
    """
    if not place or not place.strip():
        raise ValueError("Empty place query")

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    }

    # Respect Nominatim policy: include a valid identifying User-Agent and optional email
    email = os.environ.get("NOMINATIM_EMAIL")
    ua = f"MultiAgentTourismPlanner/1.0 ({email or 'no-email-supplied'})"
    headers = {"User-Agent": ua}
    if email:
        params["email"] = email

    # Simple retry/backoff for transient errors
    retries = 2
    backoff = 1.0
    for attempt in range(1, retries + 2):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            if resp.status_code == 403:
                # Provide clear guidance to the caller about why this happened
                raise RuntimeError(
                    "Nominatim returned 403 Forbidden. Ensure you set NOMINATIM_EMAIL and respect the API's usage policy."
                )
            resp.raise_for_status()
            data = resp.json()

            if not data:
                raise ValueError("place_not_found")

            first = data[0]
            lat = float(first.get("lat"))
            lon = float(first.get("lon"))
            display_name = first.get("display_name", place)
            return lat, lon, display_name

        except ValueError:
            # propagate place not found
            raise
        except RuntimeError:
            # critical API policy error; do not retry
            raise
        except requests.RequestException as e:
            if attempt <= retries:
                time.sleep(backoff)
                backoff *= 2
                continue
            raise RuntimeError(f"Geocoding request failed: {e}")

