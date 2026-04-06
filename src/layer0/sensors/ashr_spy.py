import numpy as np

def compute(prices, ashr_col, spy_col):
    # The 'Builder' already checked if these exist
    ashr = prices[ashr_col].ffill()
    spy = prices[spy_col].ffill()
    
    return np.log(ashr) - np.log(spy)



  
