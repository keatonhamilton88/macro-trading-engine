import numpy as np
import pandas as pd

def compute(prices, col1, col2):
    if col1 is None or col2 is None:
        return pd.Series(index=prices.index, dtype=float)
    
    v1 = prices[col1].ffill()
    v2 = prices[col2].ffill()
    
    # Standard Log-Differential (Growth/Inflation/Credit)
    # Note: Use v1 / v2 (no log) for vix_ratio
    return np.log(v1) - np.log(v2)


  
