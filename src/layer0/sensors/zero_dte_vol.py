import numpy as np 
import pandas as pd

def zero_dte_vol(prices):
    # 1. Safety Check: If prices is empty, return a blank Series
    if prices is None or prices.empty:
        return pd.Series(dtype=float)

  
    return pd.Series(0.0, index=prices.index, name='zero_dte_vol')


# Future Logic for the Sensor
# def zero_dte_vol_force(prices, zero_dte_data, total_vol_data):
#     # Calculate the 'Dominance' of 0DTE
#     ratio = zero_dte_data / total_vol_data
    
#     # Z-Score the ratio to see if 0DTE is 'unusually' active
#     return (ratio - ratio.rolling(20).mean()) / ratio.rolling(20).std()
