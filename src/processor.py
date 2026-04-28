import pandas as pd

def clean_conflict_data(df):
    """
    Cleans the conflict data by converting dates and handling missing values.

    Args:
        df (pd.DataFrame): The raw input data.

    Returns:
        pd.DataFrame: The cleaned data.
    """
    df = df.copy()

    # Convert date columns to datetime
    df['date_start'] = pd.to_datetime(df['date_start'])
    df['date_end'] = pd.to_datetime(df['date_end'])

    # Fill missing fatality values with 0
    death_cols = ['deaths_a', 'deaths_b', 'deaths_civilians', 'deaths_unknown']
    for col in death_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    return df

def aggregate_deaths(df):
    """
    Calculates total fatalities per event.

    Args:
        df (pd.DataFrame): The cleaned data.

    Returns:
        pd.DataFrame: Data with a new 'total_deaths' column.
    """
    df = df.copy()
    death_cols = ['deaths_a', 'deaths_b', 'deaths_civilians', 'deaths_unknown']

    # Ensure all death columns exist
    for col in death_cols:
        if col not in df.columns:
            df[col] = 0

    df['total_deaths'] = df[death_cols].sum(axis=1)
    return df
