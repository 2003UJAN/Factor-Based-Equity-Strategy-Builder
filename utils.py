import yfinance as yf

def fetch_price_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df = df[['Close']].rename(columns={"Close": "close"})
    return df

def fetch_fundamental_data(ticker):
    # Mock fundamental data for demo purposes
    # You can replace this with real AlphaVantage/Quandl API code
    return {
        "PERatio": 15,
        "EVtoEBITDA": 12,
        "PriceToBook": 3
    }
