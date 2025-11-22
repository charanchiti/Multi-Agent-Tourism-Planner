"""Terminal test harness for Multi-Agent Tourism Planner.

`app.py` is a lightweight CLI entry used for testing agents in the terminal.
For running the Streamlit web UI, run: `streamlit run streamlit.py`.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict


# Ensure project root is on sys.path so local imports work when running this script
ROOT = os.path.dirname(__file__)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.parser import parse_query
from agents.parent_agent import ParentAgent
from utils.formatter import format_results


def pretty_print_results(results: Dict[str, Any]) -> None:
    # Normalize the 'weather' and 'places' keys if present for nicer output
    print(json.dumps(results, indent=2, ensure_ascii=False))


def run_cli_query(query: str) -> None:
    parsed = parse_query(query)
    place = parsed.get("place")
    want_weather = parsed.get("want_weather")
    want_places = parsed.get("want_places")

    parent = ParentAgent()

    try:
        results = parent.run(place, want_weather=want_weather, want_places=want_places)
    except ValueError as e:
        # Map specific place_not_found error to user-facing message
        if str(e) == "place_not_found":
            print("I don’t think this place exists.")
            return
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    pretty_print_results(results)
    # Also print a concise human-friendly summary
    try:
        summary = format_results(results, want_weather=want_weather, want_places=want_places)
        print("\nSummary:\n")
        print(summary)
    except Exception:
        pass


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Terminal test harness for Multi-Agent Tourism Planner")
    parser.add_argument("query", nargs="*", help="Query string (e.g., 'Weather in Paris')")
    args = parser.parse_args()

    if args.query:
        query = " ".join(args.query)
        run_cli_query(query)
    else:
        print("No query provided. Running sample queries:\n")
        samples = [
            "Paris, France",
            "Weather in New York",
            "Things to do in Kyoto",
            "Asdfghjkl NowhereLand",
        ]
        for s in samples:
            print(f"\n--- Query: {s} ---")
            run_cli_query(s)


if __name__ == "__main__":
    main()
