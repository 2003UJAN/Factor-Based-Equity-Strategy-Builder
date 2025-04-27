import os
from dotenv import load_dotenv
import yfinance as yf
from alpha_vantage.fundamentaldata import FundamentalData

# Load environment variables from .env file
load_dotenv()

# Fetch API key from environment variable
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

if ALPHA_VANTAGE_API_KEY is None:
    raise ValueError("API Key not found. Please set the ALPHA_VANTAGE_API_KEY environment variable.")

def fetch_price_data(ticker, start_date, end_date):
    """Fetch stock price data for a given ticker from Yahoo Finance."""
    df = yf.download(ticker, start=start_date, end=end_date)
    df = df[['Close']].rename(columns={"Close": "close"})
    return df

def fetch_fundamental_data(ticker):
    """Fetch fundamental data for a given ticker from Alpha Vantage."""
    fd = FundamentalData(ALPHA_VANTAGE_API_KEY, output_format='pandas')
    
    try:
        # Fetch company overview (fundamentals like P/E ratio, EV/EBITDA, etc.)
        data, _ = fd.get_company_overview(ticker)
        
        fundamentals = {
            "PERatio": data["PERatio"].iloc[0],
            "EVtoEBITDA": data["EVtoEBITDA"].iloc[0],
            "PriceToBook": data["PriceToBook"].iloc[0]
        }
        return fundamentals
    except Exception as e:
        print(f"Error fetching fundamental data for {ticker}: {e}")
        # Return mock data in case of an error
        return {
            "PERatio": 15,
            "EVtoEBITDA": 12,
            "PriceToBook": 3
        }
