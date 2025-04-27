# app.py
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import fetch_price_data, load_uploaded_data
from backtest_engine import run_backtest
from report_generator import generate_report
from PIL import Image
import datetime

st.set_page_config(page_title="💥 Factor-Based Strategy Builder", page_icon="📈", layout="wide")
st.title("💥 Factor-Based Equity Strategy Builder")
st.markdown("Build, backtest, and export your factor strategies with professional reports!")

# Sidebar 🎛️
st.sidebar.header("Configuration 🎛️")

source = st.sidebar.radio("Data Source", ["Yahoo Finance", "Upload CSV"])

if source == "Yahoo Finance":
    symbol = st.sidebar.text_input("Stock Symbol (e.g., AAPL)", value="AAPL")
    col1, col2 = st.sidebar.columns(2)
    start_date = col1.date_input("Start Date", value=datetime.date(2020, 1, 1))
    end_date = col2.date_input("End Date", value=datetime.date(2023, 1, 1))
else:
    uploaded_file = st.sidebar.file_uploader("Upload your CSV", type=["csv"])
    symbol = "Custom Dataset"
    start_date = None
    end_date = None

factor = st.sidebar.selectbox("Factor", ["PERatio", "EVtoEBITDA", "PriceToBook"])
ascending = st.sidebar.radio("Factor Order", ["Ascending", "Descending"]) == "Ascending"

run_button = st.sidebar.button("🚀 Run Backtest")

if run_button:
    try:
        with st.spinner("Fetching data and running backtest..."):
            if source == "Yahoo Finance":
                data = fetch_price_data(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
                benchmark_data = fetch_price_data("SPY", start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
            else:
                data = load_uploaded_data(uploaded_file)
                benchmark_data = None

            buf, sharpe, returns = run_backtest(data, factor=factor, ascending=ascending, benchmark_data=benchmark_data)

        st.subheader("📊 Backtest Results")

        col1, col2 = st.columns(2)
        with col1:
            sharpe_ratio = sharpe.get('sharperatio', 0)
            st.metric(label="Sharpe Ratio 📈", value=f"{sharpe_ratio:.2f}")

        with col2:
            total_return = returns.get('rtot', 0) * 100
            st.metric(label="Total Return 💰", value=f"{total_return:.2f}%")

        st.subheader("📈 Equity Curve")
        image = Image.open(buf)
        st.image(image, caption='Backtest Plot', use_column_width=True)

        st.success("✅ Backtest Completed!")

        # Report download button
        st.subheader("📄 Download Report")
        report_path = generate_report(symbol, sharpe_ratio, total_return)
        with open(report_path, "rb") as file:
            btn = st.download_button(
                label="Download Report PDF",
                data=file,
                file_name="backtest_report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("👈 Configure your parameters and click **Run Backtest** to start!")
