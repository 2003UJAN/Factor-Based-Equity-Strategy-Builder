# app.py
import streamlit as st
from data_loader import get_fundamental_data, preprocess_fundamental_data
from backtest_engine import run_backtest
from utils import generate_dummy_price_data

st.set_page_config(page_title="📈 Factor-Based Strategy Builder", layout="wide")

st.title("💣 Factor-Based Equity Strategy Builder")
st.markdown("Create and Backtest Equity Strategies Based on Financial Ratios!")

with st.sidebar:
    st.header("🚀 Strategy Settings")
    symbol = st.text_input("Stock Symbol", "AAPL")
    factor = st.selectbox("Factor", ["PERatio", "PEGRatio", "PriceToBookRatio", "EVToEBITDA", "ReturnOnEquityTTM"])
    order = st.radio("Order (Ascending means lower is better)", ["Ascending", "Descending"])

    if st.button("🔎 Load & Backtest"):
        try:
            raw_data = get_fundamental_data(symbol)
            factors = preprocess_fundamental_data(raw_data)
            st.success(f"Successfully fetched data for {symbol}")

            price_data = generate_dummy_price_data(symbol)
            cerebro, sharpe, returns = run_backtest(
                price_data,
                factor=factor,
                ascending=(order == "Ascending")
            )

            st.subheader("📊 Backtest Results")
            st.metric(label="Sharpe Ratio", value=f"{sharpe.get('sharperatio', 0):.2f}")
            st.metric(label="Total Return", value=f"{returns.get('rnorm100', 0):.2f}%")
            st.pyplot(cerebro.plot()[0][0])

            st.subheader("🧠 Factor Values")
            st.json(factors)

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Built with 💜 using Streamlit, Backtrader, Alpha Vantage")
