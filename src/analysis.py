import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
import os
from src.war_data import get_country_metadata

def analyze_by_region(df):
    """
    Calculates number of events and total fatalities per region.

    Args:
        df (pd.DataFrame): Processed data.

    Returns:
        pd.DataFrame: Aggregated data by region.
    """
    if 'total_deaths' not in df.columns:
        raise ValueError("DataFrame must contain 'total_deaths' column. Run aggregate_deaths first.")

    region_stats = df.groupby('region').agg(
        event_count=('id', 'count'),
        total_fatalities=('total_deaths', 'sum')
    ).reset_index()

    return region_stats

def plot_fatalities_over_time(df, output_path=None):
    """
    Visualizes the trend of fatalities over time.

    Args:
        df (pd.DataFrame): Processed data.
        output_path (str, optional): Path to save the plot.
    """
    if 'total_deaths' not in df.columns:
        raise ValueError("DataFrame must contain 'total_deaths' column.")

    # Group by year
    yearly_fatalities = df.groupby('year')['total_deaths'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=yearly_fatalities, x='year', y='total_deaths', marker='o', color='#d9534f', linewidth=2.5)
    plt.title('Global Conflict Fatalities Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Total Fatalities', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)

    if output_path:
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def generate_conflict_map(df, output_path="conflict_map.html"):
    """
    Generates an interactive, responsive war map showing conflict interactions,
    hotspots, country flags, leader profiles, and event casualty details.

    Args:
        df (pd.DataFrame): Processed conflict data with latitude and longitude.
        output_path (str, optional): Path to save the interactive HTML map.

    Returns:
        folium.Map: The Folium map object.
    """
    # Base map with Dark Matter tactical tiles for war theme
    m = folium.Map(
        location=[20, 10],
        zoom_start=2.5,
        tiles=None,
        control_scale=True
    )
    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        name="Tactical Map"
    ).add_to(m)

    marker_cluster = MarkerCluster(name="Conflict Events").add_to(m)

    for _, row in df.iterrows():
        lat = row.get('latitude')
        lon = row.get('longitude')
        if pd.isna(lat) or pd.isna(lon):
            continue

        country = row.get('country', 'Unknown')
        deaths = row.get('total_deaths', 0)
        deaths_a = row.get('deaths_a', 0)
        deaths_b = row.get('deaths_b', 0)
        deaths_civ = row.get('deaths_civilians', 0)
        start_date = str(row.get('date_start', 'N/A'))[:10]
        end_date = str(row.get('date_end', 'N/A'))[:10]
        event_id = row.get('id', 'N/A')

        meta = get_country_metadata(country)

        # Popup styling with responsive, dark war theme
        popup_html = f"""
        <div style="font-family: 'Courier New', monospace; background-color: #1a1c1e; color: #e0e0e0; padding: 12px; border-radius: 8px; max-width: 280px; border: 1px solid #d9534f; box-shadow: 0 4px 12px rgba(0,0,0,0.6);">
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #444; padding-bottom: 6px; margin-bottom: 8px;">
                <h4 style="margin: 0; color: #ff4d4d; font-size: 15px; text-transform: uppercase;">{country}</h4>
                <img src="{meta['flag_url']}" style="height: 20px; border: 1px solid #fff; border-radius: 2px;" alt="flag" />
            </div>

            <p style="margin: 3px 0; font-size: 12px;"><strong>Event ID:</strong> #{event_id}</p>
            <p style="margin: 3px 0; font-size: 12px;"><strong>Dates:</strong> {start_date} to {end_date}</p>
            <p style="margin: 3px 0; font-size: 13px; color: #ff6666;"><strong>Total Fatalities:</strong> {deaths}</p>

            <div style="background-color: #2b2b2b; padding: 6px; border-radius: 4px; margin: 8px 0; font-size: 11px;">
                <div>• Side A: {deaths_a}</div>
                <div>• Side B: {deaths_b}</div>
                <div>• Civilians: {deaths_civ}</div>
            </div>

            <div style="border-top: 1px dashed #555; pt: 6px; margin-top: 6px; font-size: 11px;">
                <strong>Leader:</strong> {meta['leader']}<br/>
                <span style="color: #aaa; font-style: italic;">"{meta['nostalgia_quote']}"</span>
            </div>
        </div>
        """

        # Custom circle size based on total fatalities
        radius = 6 + min(deaths / 5, 20)
        color = '#ff3333' if deaths > 50 else ('#ff8800' if deaths > 10 else '#ffcc00')

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{country} | Fatalities: {deaths} ({start_date})",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            weight=1.5
        ).add_to(marker_cluster)

    # Inject responsive CSS styling and dark filter to map tiles
    css_injection = """
    <style>
        html, body { width: 100%; height: 100%; margin: 0; padding: 0; }
        .leaflet-container { background: #111 !important; font-family: system-ui, sans-serif; }
        .leaflet-tile-pane { filter: brightness(0.6) invert(1) contrast(3) hue-rotate(200deg) saturate(0.3) brightness(0.7); }
    </style>
    """
    m.get_root().header.add_child(folium.Element(css_injection))

    if output_path:
        m.save(output_path)

    return m
