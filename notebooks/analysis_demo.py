import os
import sys

# Add the project root to the path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import load_data
from src.processor import clean_conflict_data, aggregate_deaths
from src.analysis import analyze_by_region, plot_fatalities_over_time, generate_conflict_map
from src.ai_assistant import WarIntelligenceAI

def main():
    print("==========================================")
    print("  UCDP GED War Analysis & AI Intelligence")
    print("==========================================")

    # 1. Load Data
    print("\n1. Loading sample conflict data...")
    df = load_data()

    # 2. Process Data
    print("2. Cleaning and processing conflict data...")
    df_cleaned = clean_conflict_data(df)
    df_processed = aggregate_deaths(df_cleaned)

    # 3. Regional Statistics
    print("\n3. Regional War Fatalities & Event Statistics:")
    region_stats = analyze_by_region(df_processed)
    print(region_stats.to_string(index=False))

    # 4. Generate Visualization Chart
    print("\n4. Generating fatalities trend chart...")
    output_plot = "fatalities_trend.png"
    plot_fatalities_over_time(df_processed, output_path=output_plot)
    print(f"   -> Saved trend chart to: {output_plot}")

    # 5. Generate Interactive Tactical Map
    print("\n5. Generating interactive war interactions map...")
    output_map = "conflict_map.html"
    generate_conflict_map(df_processed, output_path=output_map)
    print(f"   -> Saved interactive map to: {output_map}")

    # 6. Test War Intelligence AI
    print("\n6. Testing War Intelligence AI Assistant...")
    ai = WarIntelligenceAI(df_processed)

    queries = [
        "Who is the leader of Ukraine?",
        "What are the fatalities in Sudan?",
        "Explain the interactive map war interactions"
    ]

    for q in queries:
        print(f"\n[USER QUESTION]: {q}")
        print(f"[AI RESPONSE]:\n{ai.ask(q)}")

    print("\n==========================================")
    print("  Demo Complete! Launch 'python app.py' to run web dashboard.")
    print("==========================================")

if __name__ == "__main__":
    main()
