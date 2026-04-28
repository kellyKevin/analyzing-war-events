# Analyzing War Events

A project providing a data science analysis of global conflict events using the UCDP Georeferenced Event Dataset (GED). This project is designed as a learning resource for Python data science, focusing on data acquisition, processing, analysis, and visualization.

## Overview

The UCDP Georeferenced Event Dataset (GED) is one of the most comprehensive datasets on organized violence, providing detailed information on individual events of conflict. This project demonstrates how to:
- Load conflict data from local CSV files.
- Clean and preprocess conflict data using `pandas`.
- Perform statistical analysis on conflict trends and fatalities.
- Create visualizations to communicate findings.

## Installation

To set up the project environment, ensure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Analysis Demo

You can run the demonstration script to see the analysis in action using sample data:

```bash
python notebooks/analysis_demo.py
```

## Project Structure

- `data/`: Contains sample datasets.
- `src/`: Core logic for data loading (from local CSV), processing, and analysis.
- `notebooks/`: Demonstration scripts and analysis examples.
- `tests/`: Unit tests for the project.
- `details.md`: In-depth documentation on the dataset and methodology.
