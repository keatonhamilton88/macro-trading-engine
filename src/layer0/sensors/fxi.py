import numpy as np

def fxi(prices):
    if "FXI" not in prices:
        return pd.Series(index=prices.index, dtype=float)
    
    fxi = prices["FXI"].ffill()
    
    return np.log(fxi)
