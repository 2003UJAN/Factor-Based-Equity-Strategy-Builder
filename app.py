# app.py
import streamlit as st
from utils import fetch_price_data
from backtest_engine import run_backtest
from PIL import Image
import datetime

st.set_page_config(page_title="📈 Factor-Based Strategy Builder", page_icon="💥", layout="wide")

st.title("💥 Factor-Based Equity Strategy Builder")
st.markdown("Build and backtest strategies based on financial ratios!")

# 🎯 Sidebar for user input
st.sidebar.header("User Configuration 🎛️")

symbol = st.sidebar.text_input("Stock Symbol (e.g., AAPL, MSFT)", value="AAPL")

col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Start Date", value=datetime.date(2020, 1, 1))
end_date = col2.date_input("End Date", value=datetime.date(2023, 1, 1))

factor = st.sidebar.selectbox("Factor to Sort By", ["PERatio", "EVtoEBITDA", "PriceToBook"])
ascending = st.sidebar.radio("Factor Order", ["Ascending", "Descending"]) == "Ascending"

run_button = st.sidebar.button("🚀 Run Backtest")

# 🎯 Main Area
if run_button:
    try:
        with st.spinner("Fetching data and running backtest..."):
            data = fetch_price_data(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
            buf, sharpe, returns = run_backtest(data, factor=factor, ascending=ascending)

        st.subheader("📊 Backtest Results")
        
        col1, col2 = st.columns(2)

        with col1:
            sharpe_ratio = sharpe.get('sharperatio', 0)
            if sharpe_ratio is not None:
                st.metric(label="Sharpe Ratio 📈", value=f"{sharpe_ratio:.2f}", delta_color="off")
            else:
                st.metric(label="Sharpe Ratio 📈", value="N/A", delta_color="off")

        with col2:
            total_return = returns.get('rtot', 0) * 100
            if total_return >= 0:
                st.metric(label="Total Return 💰", value=f"{total_return:.2f}%", delta=f"{total_return:.2f}%", delta_color="normal")
            else:
                st.metric(label="Total Return 💸", value=f"{total_return:.2f}%", delta=f"{total_return:.2f}%", delta_color="inverse")

        st.subheader("📈 Equity Curve")
        image = Image.open(buf)
        st.image(image, caption='Backtest Plot', use_column_width=True)

    except Exception as e:
        st.error(f"Error running backtest: {e}")

else:
    st.info("👈 Configure parameters on the left and click **Run Backtest**!")
