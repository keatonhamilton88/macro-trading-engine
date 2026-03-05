import yfinance as yf
import pandas as pd

# Download historical data
data = yf.download("SPY", start="2026-01-01")

print(data.head())