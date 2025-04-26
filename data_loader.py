# data_loader.py
import pandas as pd
import requests
import os

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_fundamental_data(symbol):
    """
    Fetches fundamental data for a given symbol using Alpha Vantage API
    """
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "Symbol" not in data:
        raise ValueError(f"Error fetching data for {symbol}. Check API key and symbol.")

    return data

def preprocess_fundamental_data(data):
    """
    Convert string ratios to float
    """
    relevant_fields = ["PERatio", "PEGRatio", "PriceToBookRatio", "EVToEBITDA", "ReturnOnEquityTTM"]
    clean_data = {k: float(data[k]) if k in data and data[k] != 'None' else None for k in relevant_fields}
    return clean_data
