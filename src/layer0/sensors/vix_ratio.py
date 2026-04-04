import numpy as np
import pandas as pd 

def vix_term_structure(prices):
    # 1. Safety Check: Exact yfinance tickers with ^ prefix
    if "^VIX3M" not in prices or "^VIX" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    # 2. Ratio Calculation (The 'Cleaner' Sensor)
    # Using .ffill() to prevent tiny gaps from breaking the math
    ratio = prices["^VIX3M"].ffill() / prices["^VIX"].ffill()
    
    return ratio.rename("vix_ratio")


#PCA Weighting: PCA loves this sensor because it often moves differently than the raw VIX. It captures the speed of fear.
