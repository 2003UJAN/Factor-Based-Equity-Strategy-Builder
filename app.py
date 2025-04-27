import streamlit as st
from datetime import datetime
from utils import fetch_price_data, fetch_fundamental_data

def run_backtest(ticker, start_date, end_date):
    # Fetch the stock price data
    price_data = fetch_price_data(ticker, start_date, end_date)
    
    # Fetch the fundamental data
    fundamentals = fetch_fundamental_data(ticker)
    
    # Display the results
    st.subheader(f"Fundamental Data for {ticker}")
    st.write(f"Price-to-Earnings (P/E) Ratio: {fundamentals['PERatio']}")
    st.write(f"EV/EBITDA Ratio: {fundamentals['EVtoEBITDA']}")
    st.write(f"Price-to-Book Ratio: {fundamentals['PriceToBook']}")
    
    st.subheader(f"Stock Price Data from {start_date} to {end_date}")
    st.line_chart(price_data['close'])
    
    # Placeholder for backtest result
    st.write("Performing backtest...")

    # Display basic backtest stats
    st.write("Sharpe Ratio: N/A (Backtest Logic Not Implemented)")
    st.write("Total Return: N/A (Backtest Logic Not Implemented)")

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
