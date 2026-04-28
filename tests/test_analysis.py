import pytest
import pandas as pd
from src.processor import clean_conflict_data, aggregate_deaths
from src.analysis import analyze_by_region

@pytest.fixture
def sample_df():
    data = {
        'id': [1, 2],
        'year': [2020, 2020],
        'region': ['Africa', 'Africa'],
        'date_start': ['2020-01-01', '2020-01-05'],
        'date_end': ['2020-01-01', '2020-01-06'],
        'deaths_a': [10, 5],
        'deaths_b': [5, 2],
        'deaths_civilians': [0, 10],
        'deaths_unknown': [0, 0]
    }
    return pd.DataFrame(data)

def test_clean_conflict_data(sample_df):
    cleaned_df = clean_conflict_data(sample_df)
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['date_start'])
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['date_end'])

def test_aggregate_deaths(sample_df):
    processed_df = aggregate_deaths(sample_df)
    assert 'total_deaths' in processed_df.columns
    assert processed_df.loc[0, 'total_deaths'] == 15
    assert processed_df.loc[1, 'total_deaths'] == 17

def test_analyze_by_region(sample_df):
    processed_df = aggregate_deaths(sample_df)
    region_stats = analyze_by_region(processed_df)
    assert region_stats.loc[0, 'region'] == 'Africa'
    assert region_stats.loc[0, 'event_count'] == 2
    assert region_stats.loc[0, 'total_fatalities'] == 32
