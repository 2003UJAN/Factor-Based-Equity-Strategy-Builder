import streamlit as st
import os
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv
import requests
import pandas as pd
import matplotlib.pyplot as plt

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

# Function to fetch stock price data using yfinance
def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function to plot stock price and moving averages
def plot_stock_data(stock_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(stock_data['Close'], label='Closing Price', color='blue')
    ax.set_title("Stock Price History")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    
    # Plotting moving averages
    stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()
    ax.plot(stock_data['MA50'], label='50-Day Moving Average', color='orange')
    ax.plot(stock_data['MA200'], label='200-Day Moving Average', color='green')
    
    st.pyplot(fig)

# Streamlit UI
st.title("Factor-Based Equity Strategy Builder")

st.sidebar.header("User Input")

# Ticker and Date Input
ticker = st.sidebar.text_input("Stock Ticker (e.g., MSFT)", value="MSFT")
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2021, 1, 1))

# Run backtest and show results
if st.sidebar.button("Run Backtest"):
    # Fetch fundamental data
    fundamentals = fetch_fundamental_data(ticker)
    
    # Display fundamental data
    st.subheader(f"Fundamental Data for {ticker}")
    st.write(f"Price-to-Earnings (P/E) Ratio: {fundamentals['PERatio']}")
    st.write(f"EV/EBITDA Ratio: {fundamentals['EVtoEBITDA']}")
    st.write(f"Price-to-Book Ratio: {fundamentals['PriceToBook']}")
    
    # Fetch and plot stock data
    stock_data = fetch_stock_data(ticker, start_date, end_date)
    
    if not stock_data.empty:
        plot_stock_data(stock_data)
        
        # Backtest Logic (Dummy: just using moving averages for simplicity)
        stock_data['Signal'] = 0
        stock_data['Signal'][50:] = np.where(stock_data['MA50'][50:] > stock_data['MA200'][50:], 1, 0)
        stock_data['Returns'] = stock_data['Close'].pct_change() * stock_data['Signal'].shift(1)
        stock_data['Cumulative Returns'] = (1 + stock_data['Returns']).cumprod()

        st.subheader("Backtest Results")
        st.write(f"Total Return: {stock_data['Cumulative Returns'][-1]:.2%}")
        
        # Plot cumulative returns
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(stock_data['Cumulative Returns'], label='Strategy Returns', color='red')
        ax.set_title("Cumulative Returns from Backtest")
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Return")
        ax.legend()
        st.pyplot(fig)
