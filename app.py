import streamlit as st
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment variables
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# Function to fetch real-time fundamental data from Alpha Vantage
def fetch_fundamental_data(ticker):
    url = f"https://www.alphavantage.co/query"
    
    # Parameters for Alpha Vantage API request (Company Overview)
    params = {
        'function': 'OVERVIEW',
        'symbol': ticker,
        'apikey': api_key
    }
    
    # Send request to Alpha Vantage API
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract fundamental data
        pe_ratio = float(data.get("PERatio", 0))
        ev_to_ebitda = float(data.get("EVToEBITDA", 0))
        price_to_book = float(data.get("PriceToBookRatio", 0))
        
        return {
            "PERatio": pe_ratio,
            "EVtoEBITDA": ev_to_ebitda,
            "PriceToBook": price_to_book
        }
    else:
        st.error(f"Error fetching data for {ticker}: {response.status_code}")
        return {
            "PERatio": 0,
            "EVtoEBITDA": 0,
            "PriceToBook": 0
        }

# Streamlit UI
st.title("Factor-Based Equity Strategy Builder")

st.sidebar.header("User Input")

# Ticker and Date Input
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL)", value="AAPL")
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2021, 1, 1))

# Fetch and Display Data
if st.sidebar.button("Run Backtest"):
    # Fetch fundamental data
    fundamentals = fetch_fundamental_data(ticker)
    
    # Display fundamental data
    st.subheader(f"Fundamental Data for {ticker}")
    st.write(f"Price-to-Earnings (P/E) Ratio: {fundamentals['PERatio']}")
    st.write(f"EV/EBITDA Ratio: {fundamentals['EVtoEBITDA']}")
    st.write(f"Price-to-Book Ratio: {fundamentals['PriceToBook']}")
