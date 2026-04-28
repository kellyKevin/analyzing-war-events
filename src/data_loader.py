import requests
import pandas as pd

def fetch_api_data(token, pagesize=100, page=1):
    """
    Fetches data from the UCDP GED API.

    Args:
        token (str): The UCDP access token.
        pagesize (int): Number of rows per page.
        page (int): Page number to retrieve.

    Returns:
        dict: The JSON response from the API.
    """
    url = "https://ucdpapi.pcr.uu.se/api/gedevents/25.1"
    headers = {"x-ucdp-access-token": token}
    params = {"pagesize": pagesize, "page": page}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def load_local_data(filepath):
    """
    Loads data from a local CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data.
    """
    return pd.read_csv(filepath)
