# ==========================================
# STOCK MARKET DATA ANALYZER
# ==========================================

# Import Libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# CREATE REQUIRED FOLDERS
# ==========================================

folders = [
    "data",
    "outputs",
    "images",
    "reports"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# ==========================================
# USER INPUT
# ==========================================

print("\n=================================")
print(" STOCK MARKET DATA ANALYZER ")
print("=================================\n")

ticker = input(
    "Enter Stock Ticker (Example: AAPL, TSLA, TCS.NS): "
).upper()

start_date = input(
    "Enter Start Date (YYYY-MM-DD): "
)

end_date = input(
    "Enter End Date (YYYY-MM-DD): "
)

# ==========================================
# FETCH STOCK DATA
# ==========================================

print("\nDownloading stock data...\n")

stock_data = yf.download(
    ticker,
    start=start_date,
    end=end_date
)

# ==========================================
# FIX MULTI-INDEX COLUMNS
# ==========================================

stock_data.columns = stock_data.columns.get_level_values(0)

print("\nColumns in dataset:\n")
print(stock_data.columns)

# ==========================================
# CHECK IF DATA EXISTS
# ==========================================

if stock_data.empty:
    print("No data found.")
    print("Check ticker symbol or internet connection.")
    exit()

# ==========================================
# SAVE RAW DATA
# ==========================================

raw_data_path = (
    f"data/{ticker}_raw_stock_data.csv"
)

stock_data.to_csv(raw_data_path)

print(f"Raw stock data saved to:\n{raw_data_path}")

# ==========================================
# DATA CLEANING
# ==========================================

print("\nCleaning data...\n")

stock_data.dropna(inplace=True)

stock_data.drop_duplicates(inplace=True)

# ==========================================
# DAILY RETURNS CALCULATION
# ==========================================

stock_data['Daily Return'] = (
    stock_data['Close'].pct_change()
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
# VOLATILITY CALCULATION
# ==========================================

volatility = (
    stock_data['Daily Return']
    .std()
)

# ==========================================
# HIGHEST & LOWEST PRICE
# ==========================================

highest_price = float(
    stock_data['High'].max()
)

lowest_price = float(
    stock_data['Low'].min()
)

average_close_price = float(
    stock_data['Close'].mean()
)

# ==========================================
# FINAL SUMMARY REPORT
# ==========================================

report = f"""
=========================================
STOCK MARKET ANALYSIS REPORT
=========================================

Ticker Symbol:
{ticker}

Date Range:
{start_date} to {end_date}

-----------------------------------------

Highest Stock Price:
{highest_price:.2f}

Lowest Stock Price:
{lowest_price:.2f}

Average Closing Price:
{average_close_price:.2f}

Volatility:
{volatility:.4f}

-----------------------------------------

Project Insights:

1. Moving averages help identify trends.

2. Daily return measures stock performance.

3. Volatility indicates stock risk level.

=========================================
"""

print(report)

# ==========================================
# SAVE REPORT
# ==========================================

report_path = (
    f"reports/{ticker}_analysis_report.txt"
)

with open(report_path, "w") as file:
    file.write(report)

print(f"Report saved to:\n{report_path}")

# ==========================================
# PROFESSIONAL STOCK PRICE CHART
# ==========================================

plt.figure(figsize=(15, 8))

plt.plot(
    stock_data.index,
    stock_data['Close'],
    linewidth=2,
    label='Closing Price'
)

plt.plot(
    stock_data.index,
    stock_data['20 Day MA'],
    linewidth=2,
    label='20-Day Moving Average'
)

plt.plot(
    stock_data.index,
    stock_data['50 Day MA'],
    linewidth=2,
    label='50-Day Moving Average'
)

plt.title(
    f'{ticker} Stock Price Analysis',
    fontsize=18
)

plt.xlabel(
    'Date',
    fontsize=14
)

plt.ylabel(
    'Stock Price',
    fontsize=14
)

plt.legend()

plt.grid(True)

plt.tight_layout()

moving_average_chart = (
    f"images/{ticker}_moving_average_chart.png"
)

plt.savefig(
    moving_average_chart,
    dpi=300
)

plt.show()

print(f"Chart saved to:\n{moving_average_chart}")

# ==========================================
# DAILY RETURNS DISTRIBUTION CHART
# ==========================================

plt.figure(figsize=(12, 6))

sns.histplot(
    stock_data['Daily Return'].dropna(),
    bins=50,
    kde=True
)

plt.title(
    f'{ticker} Daily Return Distribution',
    fontsize=18
)

plt.xlabel(
    'Daily Return',
    fontsize=14
)

plt.ylabel(
    'Frequency',
    fontsize=14
)

plt.grid(True)

plt.tight_layout()

returns_chart = (
    f"images/{ticker}_daily_returns_distribution.png"
)

plt.savefig(
    returns_chart,
    dpi=300
)

plt.show()

print(f"Returns chart saved to:\n{returns_chart}")

# ==========================================
# SAVE PROCESSED DATA
# ==========================================

processed_data_path = (
    f"outputs/{ticker}_processed_stock_data.csv"
)

stock_data.to_csv(processed_data_path)

print(
    f"\nProcessed data saved to:\n"
    f"{processed_data_path}"
)

# ==========================================
# COMPLETION MESSAGE
# ==========================================

print("\n=================================")
print(" ANALYSIS COMPLETED SUCCESSFULLY ")
print("=================================\n")

print("Generated Outputs:")
print("- CSV Data")
print("- Analysis Report")
print("- Moving Average Chart")
print("- Return Distribution Chart")

print("\nProject completed successfully!")