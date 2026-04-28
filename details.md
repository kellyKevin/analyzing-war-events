# Project Details: Analyzing War Events

## The UCDP Georeferenced Event Dataset (GED)

The UCDP GED is the most disaggregated dataset released by the Uppsala Conflict Data Program. It contains information on individual events of organized violence (state-based conflict, non-state conflict, and one-sided violence).

### Data Schema
Key columns used in this analysis include:
- `id`: Unique identifier for the event.
- `year`: The year the event occurred.
- `region`: The geographical region (e.g., Africa, Middle East).
- `country`: The country where the event took place.
- `date_start` & `date_end`: The time period of the event.
- `deaths_a`: Fatalities of Side A (usually the government).
- `deaths_b`: Fatalities of Side B (the opposition or second party).
- `deaths_civilians`: Number of civilians killed.
- `deaths_unknown`: Fatalities where the status is unknown.
- `latitude` & `longitude`: Geocoordinates of the event.

## Methodology

### Data Acquisition
The project focuses on analyzing conflict events using local data files. We provide a sample dataset (`data/sample_ged.csv`) to demonstrate the workflow.

### Data Processing
1. **Date Conversion**: Converting string dates to Python `datetime` objects for time-series analysis.
2. **Missing Values**: Handling cases where fatality counts or location data might be missing.
3. **Feature Engineering**: Creating a `total_deaths` column by summing `deaths_a`, `deaths_b`, `deaths_civilians`, and `deaths_unknown`.

### Analysis Goals
- **Temporal Trends**: Analyzing how the frequency and intensity (fatalities) of conflicts change over years.
- **Geospatial Distribution**: Identifying conflict hotspots by region and country.
- **Fatality Composition**: Understanding the impact on civilians versus combatants.

## Learning Objectives
- Master the `pandas` library for data manipulation.
- Learn basic data visualization techniques using `matplotlib` and `seaborn`.
