import pandas as pd
import os

def load_data(filepath=None):
    """
    Loads conflict data from a local CSV file.

    Args:
        filepath (str, optional): Path to the CSV file. If None, loads the default sample data.

    Returns:
        pd.DataFrame: The loaded data.
    """
    if filepath is None:
        # Default to the sample data in the project
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(base_dir, 'data', 'sample_ged.csv')

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found at {filepath}")

    return pd.read_csv(filepath)
