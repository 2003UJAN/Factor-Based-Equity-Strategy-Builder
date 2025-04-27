import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Function to fetch stock price data from Yahoo Finance
def fetch_price_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function to fetch fundamental data for the stock (example using mock data)
def fetch_fundamental_data(ticker):
    # You can replace this with a live API call (e.g., Alpha Vantage or Quandl) for real data
    return {
        "PERatio": 31.63,
        "EVtoEBITDA": 20.32,
        "PriceToBook": 9.62
    }

# Function to plot the stock price and moving averages
def plot_stock_data(stock_data, ticker):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(stock_data['Close'], label="Stock Price", color='blue')
    ax.plot(stock_data['MA50'], label="50-Day MA", color='orange')
    ax.plot(stock_data['MA200'], label="200-Day MA", color='green')
    ax.set_title(f"{ticker} Stock Price and Moving Averages")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    return fig

# Function to plot cumulative returns
def plot_cumulative_returns(stock_data, ticker):
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(stock_data['Cumulative Returns'], label="Cumulative Returns", color='purple')
    ax2.set_title(f"{ticker} Cumulative Returns")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Cumulative Return")
    return fig2

# Streamlit UI
st.title("Factor-Based Equity Strategy Builder")

# Sidebar for user inputs
tickers = ['MSFT', 'AAPL', 'GOOG', 'AMZN', 'TSLA', 'NFLX', 'META', 'SPY']  # List of tickers
selected_ticker = st.sidebar.selectbox("Select Stock Ticker", tickers)
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2021-01-01"))
run_button = st.sidebar.button("Run Backtest")

if run_button:
    ticker = selected_ticker  # Use the selected ticker from the dropdown

    st.write(f"### Backtest Results for {ticker}")

    # Fetching stock data
    stock_data = fetch_price_data(ticker, start_date, end_date)

    # Fetch and display fundamental data
    fundamental_data = fetch_fundamental_data(ticker)
    st.write(f"#### Fundamental Data for {ticker}")
    st.write(f"Price-to-Earnings (P/E) Ratio: {fundamental_data['PERatio']}")
    st.write(f"EV/EBITDA Ratio: {fundamental_data['EVtoEBITDA']}")
    st.write(f"Price-to-Book Ratio: {fundamental_data['PriceToBook']}")

    # Calculate Moving Averages
    stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()

    # Initialize Signal column
    stock_data['Signal'] = 0
    stock_data.iloc[50:, stock_data.columns.get_loc('Signal')] = np.where(
        stock_data['MA50'][50:] > stock_data['MA200'][50:], 1, 0
    )

    # Calculate Returns based on the Signal column
    stock_data['Returns'] = stock_data['Close'].pct_change()
    stock_data['Returns'] = stock_data['Returns'].shift(-1) * stock_data['Signal']

    # Fill NaN values in Returns
    stock_data['Returns'].fillna(0, inplace=True)

    # Calculate cumulative returns from the strategy
    stock_data['Cumulative Returns'] = (1 + stock_data['Returns']).cumprod()

    # Display Total Return (last cumulative return value)
    total_return = stock_data['Cumulative Returns'].iloc[-1] - 1  # Subtract 1 to show net return
    st.write(f"Total Return: {total_return:.2%}")

    # Plot the stock price, moving averages, and cumulative returns
    fig1 = plot_stock_data(stock_data, ticker)
    st.pyplot(fig1)

    fig2 = plot_cumulative_returns(stock_data, ticker)
    st.pyplot(fig2)
