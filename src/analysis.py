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
    hotspots, interaction vectors, country flags, leader profiles, and event details.

    Args:
        df (pd.DataFrame): Processed conflict data with latitude and longitude.
        output_path (str, optional): Path to save the interactive HTML map.

    Returns:
        folium.Map: The Folium map object.
    """
    # Base map with standard OSM tiles styled dark via CSS filter
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

    # Disable clustering at zoom level 5 for seamless marker interaction
    marker_cluster = MarkerCluster(
        name="Conflict Hotspots",
        options={'disableClusteringAtZoom': 5, 'maxClusterRadius': 40}
    ).add_to(m)

    points = []

    for _, row in df.iterrows():
        lat = row.get('latitude')
        lon = row.get('longitude')
        if pd.isna(lat) or pd.isna(lon):
            continue

        points.append((lat, lon))
        country = row.get('country', 'Unknown')
        deaths = row.get('total_deaths', 0)
        deaths_a = row.get('deaths_a', 0)
        deaths_b = row.get('deaths_b', 0)
        deaths_civ = row.get('deaths_civilians', 0)
        start_date = str(row.get('date_start', 'N/A'))[:10]
        end_date = str(row.get('date_end', 'N/A'))[:10]
        event_id = row.get('id', 'N/A')

        meta = get_country_metadata(country)

        # Tactical Popup Card
        popup_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #121418; color: #e0e6ed; padding: 14px; border-radius: 8px; width: 260px; border: 1px solid #d93838; box-shadow: 0 4px 15px rgba(0,0,0,0.7);">
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #333a45; padding-bottom: 6px; margin-bottom: 10px;">
                <h4 style="margin: 0; color: #ff4d4d; font-size: 15px; font-weight: 700; text-transform: uppercase;">{country}</h4>
                <img src="{meta['flag_url']}" style="height: 18px; border-radius: 2px; border: 1px solid #555;" alt="flag" />
            </div>

            <div style="font-size: 12px; margin-bottom: 8px; line-height: 1.6;">
                <div><strong>Event ID:</strong> #{event_id}</div>
                <div><strong>Timeline:</strong> {start_date} to {end_date}</div>
                <div style="color: #ff6666; font-weight: 700; margin-top: 2px;"><strong>Total Fatalities:</strong> {deaths}</div>
            </div>

            <div style="background-color: #1e2229; padding: 8px; border-radius: 6px; margin-bottom: 10px; font-size: 11px; border-left: 3px solid #ff9f43;">
                <div style="font-weight: 700; color: #ff9f43; margin-bottom: 4px;">WAR INTERACTION BREAKDOWN</div>
                <div>• Side A Fatalities: {deaths_a}</div>
                <div>• Side B Fatalities: {deaths_b}</div>
                <div>• Civilian Casualties: {deaths_civ}</div>
            </div>

            <div style="border-top: 1px dashed #333a45; padding-top: 8px; font-size: 11px; line-height: 1.4;">
                <div style="font-weight: 700; color: #54a0ff;">Leader: {meta['leader']}</div>
                <div style="color: #888; font-style: italic; margin-top: 2px;">"{meta['nostalgia_quote']}"</div>
            </div>
        </div>
        """

        radius = 7 + min(deaths / 4, 18)
        color = '#ff3838' if deaths > 40 else ('#ff9f43' if deaths > 10 else '#feca57')

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{country} (Event #{event_id}) | Fatalities: {deaths}",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            weight=2
        ).add_to(marker_cluster)

    # Add War Interaction Connecting Lines between consecutive conflict events in same country/region
    if len(points) > 1:
        interaction_group = folium.FeatureGroup(name="War Interaction Lines").add_to(m)
        # Group points by country and draw interaction vectors between conflict hotspots
        for country, group in df.groupby('country'):
            coords = group[['latitude', 'longitude']].dropna().values.tolist()
            if len(coords) > 1:
                folium.PolyLine(
                    locations=coords,
                    color='#d93838',
                    weight=2,
                    opacity=0.7,
                    dash_array='6, 6',
                    tooltip=f"War Interaction Line: {country}"
                ).add_to(interaction_group)

    # Inject responsive CSS styling and dark filter to map tiles
    css_injection = """
    <style>
        html, body { width: 100%; height: 100%; margin: 0; padding: 0; overflow: hidden; }
        .leaflet-container { background: #0f1115 !important; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        .leaflet-tile-pane { filter: brightness(0.65) invert(1) contrast(2.5) hue-rotate(200deg) saturate(0.3); }
        .leaflet-popup-content-wrapper { background: transparent !important; box-shadow: none !important; padding: 0 !important; }
        .leaflet-popup-tip { background: #121418 !important; border: 1px solid #d93838 !important; }
    </style>
    """
    m.get_root().header.add_child(folium.Element(css_injection))

    if output_path:
        m.save(output_path)

    return m
