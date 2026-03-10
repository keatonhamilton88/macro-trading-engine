import numpy as np
import pandas as pd 

def spx_gex(prices):
    
     if not prices.empty:
        return pd.Series(0.0, index=prices.index, name='spx_gex')
    else:
        return pd.Series(dtype=float)
