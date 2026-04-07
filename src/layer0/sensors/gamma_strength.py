import pandas as pd
import numpy as np

# In src/layer0/sensors/gamma_strength.py
def compute(prices, price_col, col2=None):
    # We find the 'GEX' or 'Flip' column manually here to keep the loop simple
    flip_col = next((c for c in prices.columns if "GEX" in c.upper() or "FLIP" in c.upper()), None)
    
    if price_col is None or flip_col is None:
        return pd.Series(index=prices.index, dtype=float)
    
    dist = (prices[price_col] - prices[flip_col]) / prices[flip_col]
    return np.tanh(dist / 0.02)





