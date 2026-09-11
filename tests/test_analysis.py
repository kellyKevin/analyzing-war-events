import pytest
import pandas as pd
from src.processor import clean_conflict_data, aggregate_deaths
from src.analysis import analyze_by_region, generate_conflict_map
from src.ai_assistant import WarIntelligenceAI
from src.war_data import get_country_metadata, WAR_METADATA

@pytest.fixture
def sample_df():
    data = {
        'id': [1, 2, 3],
        'year': [2020, 2020, 2022],
        'region': ['Africa', 'Africa', 'Europe'],
        'country': ['Ethiopia', 'Ethiopia', 'Ukraine'],
        'date_start': ['2020-01-01', '2020-01-05', '2022-02-24'],
        'date_end': ['2020-01-01', '2020-01-06', '2022-02-24'],
        'deaths_a': [10, 5, 50],
        'deaths_b': [5, 2, 30],
        'deaths_civilians': [0, 10, 10],
        'deaths_unknown': [0, 0, 10],
        'latitude': [9.145, 9.150, 50.450],
        'longitude': [40.489, 40.490, 30.523]
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
    assert processed_df.loc[2, 'total_deaths'] == 100

def test_analyze_by_region(sample_df):
    processed_df = aggregate_deaths(sample_df)
    region_stats = analyze_by_region(processed_df)
    assert 'Africa' in region_stats['region'].values
    assert 'Europe' in region_stats['region'].values

def test_war_metadata():
    meta = get_country_metadata('Ukraine')
    assert meta['country'] == 'Ukraine'
    assert 'Zelenskyy' in meta['leader']
    assert meta['flag_url'].startswith('https://')

    default_meta = get_country_metadata('Unknown Land')
    assert default_meta['country'] == 'Unknown Land'

def test_generate_conflict_map(sample_df, tmp_path):
    processed_df = aggregate_deaths(sample_df)
    map_file = tmp_path / "test_map.html"
    m = generate_conflict_map(processed_df, output_path=str(map_file))
    assert m is not None
    assert map_file.exists()
    assert map_file.stat().st_size > 0

def test_ai_assistant(sample_df):
    processed_df = aggregate_deaths(sample_df)
    ai = WarIntelligenceAI(processed_df)

    res_leader = ai.ask("Who is the leader of Ukraine?")
    assert "Zelenskyy" in res_leader

    res_deaths = ai.ask("How many deaths in Ethiopia?")
    assert "32" in res_deaths or "Casualty" in res_leader or "32" in res_deaths

    res_map = ai.ask("Show map details")
    assert "Map" in res_map or "tactical map" in res_map

    res_invalid = ai.ask("")
    assert "valid question" in res_invalid
