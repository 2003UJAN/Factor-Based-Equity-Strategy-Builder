import streamlit as st
from datetime import datetime
import pandas as pd
from utils import fetch_price_data, fetch_fundamental_data
import numpy as np

def calculate_sharpe_ratio(price_data):
    """Calculate the Sharpe Ratio of a given stock's price data."""
    # Calculate daily returns
    price_data['daily_returns'] = price_data['close'].pct_change()
    
    # Calculate the average daily return and standard deviation of daily returns
    avg_daily_return = price_data['daily_returns'].mean()
    daily_return_std = price_data['daily_returns'].std()
    
    # Assuming a risk-free rate of 0% for simplicity
    sharpe_ratio = avg_daily_return / daily_return_std if daily_return_std != 0 else np.nan
    return sharpe_ratio

def calculate_total_return(price_data):
    """Calculate total return of the stock over the backtest period."""
    # Calculate the total return (percentage change from first to last price)
    total_return = (price_data['close'][-1] / price_data['close'][0] - 1) * 100
    return total_return

def run_backtest(ticker, start_date, end_date):
    # Fetch the stock price data
    price_data = fetch_price_data(ticker, start_date, end_date)
    
    # Fetch the fundamental data
    fundamentals = fetch_fundamental_data(ticker)
    
    # Display fundamental data
    st.subheader(f"Fundamental Data for {ticker}")
    st.write(f"Price-to-Earnings (P/E) Ratio: {fundamentals['PERatio']}")
    st.write(f"EV/EBITDA Ratio: {fundamentals['EVtoEBITDA']}")
    st.write(f"Price-to-Book Ratio: {fundamentals['PriceToBook']}")
    
    # Display the stock price data
    st.subheader(f"Stock Price Data from {start_date} to {end_date}")
    st.line_chart(price_data['close'])
    
    # Perform backtest (Buy and Hold strategy)
    sharpe_ratio = calculate_sharpe_ratio(price_data)
    total_return = calculate_total_return(price_data)
    
    # Display the results of the backtest
    st.subheader("Backtest Results")
    st.write(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    st.write(f"Total Return: {total_return:.2f}%")

# Streamlit UI
st.title("Factor-Based Equity Strategy Builder")

st.sidebar.header("User Input")

# Ticker, Date, and Strategy Input
ticker = st.sidebar.text_input("Stock Ticker (e.g., AAPL)", value="AAPL")
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime(2021, 1, 1))

# Run the backtest button
if st.sidebar.button("Run Backtest"):
    run_backtest(ticker, start_date, end_date)
