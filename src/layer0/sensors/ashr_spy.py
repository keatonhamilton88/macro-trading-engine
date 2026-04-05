import numpy as np
import pandas as pd

def ashr_spy(prices):
    # 1. Find the actual column names (handles 'ASHR' or 'ashr')
    ashr_col = next((c for c in prices.columns if c.upper() == "ASHR"), None)
    spy_col = next((c for c in prices.columns if c.upper() == "SPY"), None)
    
    # 2. Safety Check: If either is missing, return blank
    if ashr_col is None or spy_col is None:
        return pd.Series(index=prices.index, dtype=float)

    # 3. Use the dynamic 'ticker' variables you just found
    ashr = prices[ashr_col].ffill()
    spy = prices[spy_col].ffill()

    # 4. Calculation: Log Ratio (Growth Sensor)
    return np.log(ashr) - np.log(spy)


  
