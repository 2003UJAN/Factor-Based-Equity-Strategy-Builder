import streamlit as st
import pandas as pd
from utils import fetch_price_data, fetch_fundamental_data
from backtest_engine import run_backtest
from ml_model import train_predict
from optimizer import optimize_strategy
import plotly.graph_objects as go

st.set_page_config(page_title="📈 Factor Strategy Builder", page_icon="📈", layout="wide")

st.title("📈 Factor-Based Equity Strategy Builder")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT)", value="AAPL")

col1, col2 = st.columns(2)
start_date = col1.date_input("Start Date", pd.to_datetime('2018-01-01'))
end_date = col2.date_input("End Date", pd.to_datetime('2023-12-31'))

factor = st.selectbox("Choose Factor", ["PERatio", "EVtoEBITDA", "PriceToBook"])
ascending = st.radio("Factor Sorting", ["Low to High", "High to Low"]) == "Low to High"

if st.button("🚀 Run Backtest"):
    try:
        data = fetch_price_data(ticker, start_date, end_date)
        fundamentals = fetch_fundamental_data(ticker)
        results, sharpe, total_return = run_backtest(data, fundamentals, factor, ascending)
        
        st.success("Backtest Completed!")

        # Metrics
        st.metric(label="📈 Sharpe Ratio", value=f"{sharpe.get('sharperatio', 'N/A'):.2f}")
        st.metric(label="💰 Total Return", value=f"{total_return:.2f}%")

        # Interactive Chart
        st.subheader("📊 Interactive Equity Curve")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=results.index, y=results['equity_curve'], mode='lines', name='Equity Curve'))
        fig.update_layout(title="Equity Curve", xaxis_title="Date", yaxis_title="Portfolio Value")
        st.plotly_chart(fig, use_container_width=True)

        # ML Model
        st.subheader("🧠 ML Model Accuracy")
        accuracy = train_predict(data)
        st.metric(label="Prediction Accuracy 🎯", value=f"{accuracy*100:.2f}%")

        # Optimizer
        if st.button("🔍 Find Best Strategy"):
            with st.spinner("Optimizing..."):
                best_params, best_score = optimize_strategy(data)
            st.success(f"Best Factor: {best_params[0]} | Ascending: {best_params[1]} | Sharpe: {best_score:.2f}")

    except Exception as e:
        st.error(f"Error: {e}")
