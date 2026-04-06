import numpy as np
import pandas as pd 

def compute(prices, ashr_col, spy_col):
    if ashr_col is None or spy_col is None:
        return pd.Series(index=prices.index, dtype=float)
    
    ashr = prices[ashr_col].ffill()
    spy = prices[spy_col].ffill()
    return np.log(ashr) - np.log(spy)

  
