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

# Streamlit UI
st.title("Factor-Based Equity Strategy Builder")

# Sidebar for user inputs
ticker = st.sidebar.text_input("Enter Stock Ticker", "MSFT")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2021-01-01"))

# Fetching stock data
stock_data = fetch_price_data(ticker, start_date, end_date)

# Display stock data and fundamental ratios
st.write(f"### Stock Data for {ticker}")
st.write(stock_data.tail())

# Fetch and display fundamental data
fundamental_data = fetch_fundamental_data(ticker)
st.write(f"### Fundamental Data for {ticker}")
st.write(f"Price-to-Earnings (P/E) Ratio: {fundamental_data['PERatio']}")
st.write(f"EV/EBITDA Ratio: {fundamental_data['EVtoEBITDA']}")
st.write(f"Price-to-Book Ratio: {fundamental_data['PriceToBook']}")

# Calculate Moving Averages
stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()

# Initialize Signal column
stock_data['Signal'] = 0

# Use .iloc for assignment to avoid SettingWithCopyWarning
stock_data.iloc[50:, stock_data.columns.get_loc('Signal')] = np.where(
    stock_data['MA50'][50:] > stock_data['MA200'][50:], 1, 0
)

# Calculate returns based on the Signal column
stock_data['Returns'] = stock_data['Close'].pct_change() * stock_data['Signal'].shift(1)

# Calculate cumulative returns from the strategy
stock_data['Cumulative Returns'] = (1 + stock_data['Returns']).cumprod()

# Display results
st.write(f"### Backtest Results for {ticker}")
st.write(f"Total Return: {stock_data['Cumulative Returns'][-1]:.2%}")

# Plot the stock price and moving averages
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(stock_data['Close'], label="Stock Price", color='blue')
ax.plot(stock_data['MA50'], label="50-Day MA", color='orange')
ax.plot(stock_data['MA200'], label="200-Day MA", color='green')
ax.set_title(f"{ticker} Stock Price and Moving Averages")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()

# Show the plot in Streamlit
st.pyplot(fig)

# Plot the cumulative returns of the strategy
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(stock_data['Cumulative Returns'], label="Cumulative Returns", color='purple')
ax2.set_title(f"{ticker} Cumulative Returns")
ax2.set_xlabel("Date")
ax2.set_ylabel("Cumulative Return")
st.pyplot(fig2)
