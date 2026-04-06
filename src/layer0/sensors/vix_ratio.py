import numpy as np
import pandas as pd

def compute(prices, col1):
    if col1 is None: 
        return pd.Series(index=prices.index, dtype=float)
    
    data = prices[col1].ffill()
    
    # Note: Remove np.log() for gamma_strength, spx_gex, and put_call_ratio
    return data 



#PCA Weighting: PCA loves this sensor because it often moves differently than the raw VIX. It captures the speed of fear.
