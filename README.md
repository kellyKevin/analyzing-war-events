# Analyzing War Events

A comprehensive Python data science and war intelligence platform for analyzing global conflict events using the UCDP Georeferenced Event Dataset (GED). Features interactive geospatial mapping, responsive dark-themed tactical dashboards, country flag and leader historical archives, and a War Intelligence AI Assistant.

## Overview

The UCDP Georeferenced Event Dataset (GED) provides disaggregated, individual conflict event data. This application transforms raw georeferenced data into an immersive interactive experience:
- **Interactive War Map**: Tactical dark map rendering conflict locations, severity clusters, side A/B/civilian casualty tooltips, and country flags.
- **War Intelligence AI Assistant**: AI Q&A bot answering user queries regarding conflict fatalities, historical context, leader profiles, and global trends.
- **Leader & Country Gallery**: Archival photos, country flags, leadership roles, and historical reflective quotes for nations involved in conflict.
- **Cross-Device Responsive Dashboard**: Dark war UI compatible with desktop, tablet, and mobile browsers.

## Installation

To set up the project environment and dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Web App & Interactive Dashboard

To launch the full responsive Web Application with the interactive map and War Intelligence AI Assistant:

```bash
python app.py
```
Then navigate to `http://localhost:5000` in your web browser.

### Running the Analysis & AI Demo Script

You can also run the CLI analysis demo to test data processing, map generation, and the AI Assistant:

```bash
python notebooks/analysis_demo.py
```

### Running Tests

To verify all system modules, run pytest:

```bash
python -m pytest tests/test_analysis.py
```

## Project Structure

- `app.py`: Flask web application server with API endpoints.
- `src/`: Core logic and AI modules.
  - `data_loader.py`: Loads conflict dataset from local CSV.
  - `processor.py`: Cleans and aggregates event fatalities.
  - `analysis.py`: Regional statistical analysis and Folium interactive map visualizer.
  - `ai_assistant.py`: Natural language query processing engine for war intelligence Q&A.
  - `war_data.py`: Metadata registry containing country flags, leader photos, and historical context.
- `templates/`: Jinja2 HTML templates for the dashboard UI (`index.html`).
- `static/`: CSS styling (`style.css`), JavaScript frontend chat logic (`main.js`), and generated map assets.
- `data/`: Sample UCDP GED dataset (`sample_ged.csv`).
- `notebooks/`: CLI demonstration scripts.
- `tests/`: Automated unit tests.
