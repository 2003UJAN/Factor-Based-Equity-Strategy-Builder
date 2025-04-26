# utils.py
import pandas as pd

def generate_dummy_price_data(symbol, start='2020-01-01', end='2023-01-01'):
    dates = pd.date_range(start=start, end=end)
    prices = pd.Series(100 + (pd.Series(range(len(dates))) * 0.5).values, index=dates)
    df = pd.DataFrame({'close': prices})
    df.index.name = 'date'
    return df
