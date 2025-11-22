"""Streamlit web UI for Multi-Agent Tourism Planner.

Run with: `streamlit run streamlit.py`
"""
from typing import Any, Dict
import streamlit as st

from utils.parser import parse_query
from utils.formatter import format_results
from agents.parent_agent import ParentAgent


st.set_page_config(page_title="Multi-Agent Tourism Planner", layout="wide")

# Small visual tweaks (typography + spacing)
st.markdown(
    """
    <style>
    .title {font-size:32px; font-weight:700; margin-bottom:6px;}
    .subtitle {color: #6b7280; margin-top:0; margin-bottom:18px}
    .stButton>button {height:44px}
    /* make text input visually match button height for alignment */
    .stTextInput>div>div>input, .stTextInput>div>div>textarea {
        height:44px !important;
        padding:8px 12px !important;
        font-size:16px !important;
        box-sizing: border-box !important;
    }
    /* summary card styling */
    .summary-card {
        background: linear-gradient(180deg, #ffffff, #f8fafc);
        border: 1px solid #e6eef6;
        border-radius: 10px;
        padding: 18px;
        margin-top: 12px;
        box-shadow: 0 6px 18px rgba(15,23,42,0.06);
        font-size: 16px;
        line-height: 1.5;
    }
    .summary-card h3 {margin:0 0 8px 0; font-size:18px}
    .summary-card p {margin:0}
    </style>
    """,
    unsafe_allow_html=True,
)


def render_weather_section(weather_data: Dict[str, Any]) -> None:
    st.subheader("Weather results")
    if "weather_error" in weather_data:
        st.error(weather_data["weather_error"])
        return

    raw_w = weather_data.get("weather")
    # raw_w could be a dict returned by WeatherAgent: {"place":..., "lat":..., "lon":..., "weather":{...}}
    if isinstance(raw_w, dict):
        child = raw_w
        w = child.get("weather") or {}
        place_label = child.get("place") or weather_data.get("input_place")
        lat = child.get("lat")
        lon = child.get("lon")
    else:
        # fallback: parent-level fields (older shape)
        w = raw_w or {}
        place_label = weather_data.get("place") or weather_data.get("input_place")
        lat = weather_data.get("lat")
        lon = weather_data.get("lon")

    if not w:
        st.info("No weather data available.")
        return

    with st.expander(f"Weather for {place_label}", expanded=True):
        st.markdown(f"**Location:** {place_label} ({lat}, {lon})")
        st.markdown(f"**Time:** {w.get('time')}")
        st.markdown(f"**Temperature:** {w.get('temperature')} °C")
        st.markdown(f"**Wind speed:** {w.get('windspeed')} m/s")


def render_places_section(places_data: Dict[str, Any]) -> None:
    st.subheader("Places results")
    if "places_error" in places_data:
        st.error(places_data["places_error"])
        return

    raw_places = places_data.get("places")
    # `raw_places` may be either:
    # - a dict produced by PlacesAgent: {"place": ..., "places": [...]}
    # - a list of place dicts (older shape)
    if isinstance(raw_places, dict):
        place_label = raw_places.get("place")
        places = raw_places.get("places") or []
    else:
        place_label = places_data.get("place") or places_data.get("input_place")
        places = raw_places or []

    if not places:
        st.info("No places found nearby.")
        return

    with st.expander(f"Places around {place_label}", expanded=True):
        for p in places:
            # guard if element is unexpectedly a string
            if not isinstance(p, dict):
                st.markdown(f"- {str(p)}")
                continue
            st.markdown(f"- **{p.get('name')}** — {p.get('type')}")


def main() -> None:
    st.title("Multi-Agent Tourism Planner ✈️ 🗺️")

    st.write("Enter a place or ask a travel question (e.g., 'Weather in Paris', 'Things to do in Kyoto')")

    # Use a form so the input and the Search button align and respond to Enter key
    with st.form(key="search_form"):
        row1, row2 = st.columns([10, 2])
        with row1:
            # default query requested by user
            user_input = st.text_input("", value="Weather in Bengaluru", placeholder="Enter a place or ask a travel question")
        with row2:
            search_clicked = st.form_submit_button("Search")

    col1, col2 = st.columns([1, 1])

    if search_clicked:
        # ensure non-empty
        user_input = (user_input or "").strip()
        if not user_input:
            st.warning("Please enter a place or travel question before searching.")
            return
        parsed = parse_query(user_input)
        place = parsed.get("place")
        want_weather = parsed.get("want_weather")
        want_places = parsed.get("want_places")

        parent = ParentAgent()

        with st.spinner("Orchestrating agents and calling APIs..."):
            try:
                results = parent.run(place, want_weather=want_weather, want_places=want_places)
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                return

        # Render into two columns
        with col1:
            if want_weather:
                render_weather_section(results)
        with col2:
            if want_places:
                render_places_section(results)

        # Also show a clean, human-friendly summary assembled locally (styled card)
        try:
            summary = format_results(results, want_weather=want_weather, want_places=want_places) or ""
            # convert newlines to <br/> for HTML rendering
            safe_html_summary = summary.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
            card_html = f"""
            <div class='summary-card'>
              <h3>Summary</h3>
              <p>{safe_html_summary}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Failed to format summary: {e}")


if __name__ == "__main__":
    main()
