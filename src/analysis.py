import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    sns.lineplot(data=yearly_fatalities, x='year', y='total_deaths', marker='o')
    plt.title('Global Conflict Fatalities Over Time')
    plt.xlabel('Year')
    plt.ylabel('Total Fatalities')
    plt.grid(True)

    if output_path:
        plt.savefig(output_path)
        plt.close()
    else:
        plt.show()
