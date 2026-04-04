import numpy as np
import pandas as pd 

def spx_gex(prices):
    # 1. Safety Check: If prices is empty, return a blank Series
    if prices is None or prices.empty:
        return pd.Series(dtype=float)

    # 2. Placeholder: Return 0.0 for now until you link your GEX source.
    # Note: Using name='spx_gex' helps your PCA engine identify this column later.
    return pd.Series(0.0, index=prices.index, name='spx_gex')


# The PCA Warning: As soon as you are ready to test your PCA Engine, 
# you must replace the 0.0 with actual (or mock) numbers. 
# If a column in your PCA matrix is all zeros, 
# the math will fail because there is no "variance" to analyze.

# MOCK DATA: Random GEX values between -5 Billion and +5 Billion
# mock_gex = np.random.uniform(-5e9, 5e9, size=len(prices))
# return pd.Series(mock_gex, index=prices.index, name='spx_gex')
