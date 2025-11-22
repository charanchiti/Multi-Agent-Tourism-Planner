# Multi-Agent Tourism Planner (LangChain + Streamlit)

This project implements a simple multi-agent tourism planner for an internship evaluation. It uses LangChain tools to wrap external APIs (Nominatim, Open-Meteo, Overpass) and a parent orchestrator agent that calls two child agents (WeatherAgent and PlacesAgent). A Streamlit frontend allows users to enter a place or travel query and view weather and places results.

## Folder structure

project/
│── app.py
│── agents/
│   ├── parent_agent.py
│   ├── weather_agent.py
│   ├── places_agent.py
│── tools/
│   ├── geocode_tool.py
│   ├── weather_tool.py
│   ├── places_tool.py
│── services/
│   ├── geocode_service.py
│   ├── weather_service.py
│   ├── places_service.py
│── utils/
│   ├── parser.py
│── requirements.txt
│── README.md

## Setup

1. Create a virtual environment (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the Streamlit web UI locally:

```powershell
streamlit run streamlit.py
```

4. Run quick terminal tests (CLI harness):

```powershell
python app.py "Weather in Paris"
python app.py  # runs sample queries
```

## Notes
- No external LLM provider is required. LangChain is used for the `Tool` wrappers around API functions.
- The agents always call external APIs for factual information. If a place is not found, the app returns: "I don’t think this place exists."

## Deploying to Streamlit Cloud

1. Push the `project/` folder to a repository.
2. On Streamlit Cloud, connect the repo and set the main file to `app.py`.
3. Add a `requirements.txt` (already included). Streamlit Cloud will install dependencies.

## API Rate Limits and Etiquette
- These public APIs have rate limits. Use thoughtfully and avoid rapid polling.
