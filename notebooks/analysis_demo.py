import os
import sys

# Add the project root to the path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import load_data
from src.processor import clean_conflict_data, aggregate_deaths
from src.analysis import analyze_by_region, plot_fatalities_over_time

def main():
    print("--- UCDP GED Analysis Demo ---")

    # 1. Load Data
    print("Loading sample data...")
    df = load_data()

    # 2. Process Data
    print("Processing data...")
    df_cleaned = clean_conflict_data(df)
    df_processed = aggregate_deaths(df_cleaned)

    # 3. Analyze Data
    print("\nRegional Statistics:")
    region_stats = analyze_by_region(df_processed)
    print(region_stats)

    # 4. Visualize Data
    print("\nGenerating visualization...")
    output_plot = "fatalities_trend.png"
    plot_fatalities_over_time(df_processed, output_path=output_plot)
    print(f"Plot saved as {output_plot}")

    print("\nAnalysis Complete.")

if __name__ == "__main__":
    main()
