# utils.py
import pandas as pd
import yfinance as yf

def fetch_price_data(symbol, start='2020-01-01', end='2023-01-01'):
    data = yf.download(symbol, start=start, end=end)
    if data.empty:
        raise ValueError("No data fetched. Check symbol and date range.")
    data = data[['Close']]
    data.rename(columns={"Close": "close"}, inplace=True)
    return data

def load_uploaded_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    data.columns = [col.lower() for col in data.columns]
    if 'close' not in data.columns:
        raise ValueError("CSV must contain a 'close' column.")
    data.index = pd.to_datetime(data['date'], errors='coerce')
    return data
