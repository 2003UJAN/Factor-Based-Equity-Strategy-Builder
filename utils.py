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
