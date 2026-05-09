# ==========================================
# STREAMLIT STOCK MARKET DASHBOARD
# ==========================================

# Import Libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# DASHBOARD TITLE
# ==========================================

st.title("Stock Market Data Analyzer")

st.write(
    "Analyze stock prices, moving averages, "
    "and financial trends using Python."
)

# ==========================================
# USER INPUTS
# ==========================================

ticker = st.text_input(
    "Enter Stock Ticker",
    "AAPL"
)

start_date = st.date_input(
    "Select Start Date"
)

end_date = st.date_input(
    "Select End Date"
)

# ==========================================
# ANALYZE BUTTON
# ==========================================

if st.button("Analyze Stock"):

    # ==========================================
    # DOWNLOAD STOCK DATA
    # ==========================================

    stock_data = yf.download(
        ticker,
        start=start_date,
        end=end_date
    )

    # ==========================================
    # FIX MULTI-INDEX ISSUE
    # ==========================================

    stock_data.columns = (
        stock_data.columns.get_level_values(0)
    )

    # ==========================================
    # CHECK EMPTY DATA
    # ==========================================

    if stock_data.empty:

        st.error(
            "No stock data found. "
            "Check ticker symbol."
        )

    else:

        # ==========================================
        # DISPLAY DATA
        # ==========================================

        st.subheader("Stock Dataset Preview")

        st.dataframe(
            stock_data.head()
        )

        # ==========================================
        # MOVING AVERAGES
        # ==========================================

        stock_data['20 Day MA'] = (
            stock_data['Close']
            .rolling(window=20)
            .mean()
        )

        stock_data['50 Day MA'] = (
            stock_data['Close']
            .rolling(window=50)
            .mean()
        )

        # ==========================================
        # DAILY RETURNS
        # ==========================================

        stock_data['Daily Return'] = (
            stock_data['Close']
            .pct_change()
        )

        # ==========================================
        # VOLATILITY
        # ==========================================

        volatility = (
            stock_data['Daily Return']
            .std()
        )

        # ==========================================
        # PRICE CHART
        # ==========================================

        st.subheader(
            "Stock Price & Moving Averages"
        )

        fig, ax = plt.subplots(
            figsize=(14, 7)
        )

        ax.plot(
            stock_data.index,
            stock_data['Close'],
            label='Closing Price'
        )

        ax.plot(
            stock_data.index,
            stock_data['20 Day MA'],
            label='20-Day MA'
        )

        ax.plot(
            stock_data.index,
            stock_data['50 Day MA'],
            label='50-Day MA'
        )

        ax.set_title(
            f'{ticker} Stock Analysis'
        )

        ax.set_xlabel('Date')

        ax.set_ylabel('Stock Price')

        ax.legend()

        ax.grid(True)

        st.pyplot(fig)

        # ==========================================
        # SHOW METRICS
        # ==========================================

        st.subheader(
            "Financial Insights"
        )

        st.write(
            f"Highest Price: "
            f"{stock_data['High'].max():.2f}"
        )

        st.write(
            f"Lowest Price: "
            f"{stock_data['Low'].min():.2f}"
        )

        st.write(
            f"Average Close Price: "
            f"{stock_data['Close'].mean():.2f}"
        )

        st.write(
            f"Volatility: "
            f"{volatility:.4f}"
        )

        # ==========================================
        # SUCCESS MESSAGE
        # ==========================================

        st.success(
            "Analysis Completed Successfully!"
        )