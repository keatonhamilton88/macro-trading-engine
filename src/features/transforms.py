import pandas as pd
import numpy as np

def zscore_sensor(series, lookback=252, is_return=True):
    if is_return:
        data = series.pct_change()
    else:
        data = series

    # 1. This calculates the correct minimum (10 for Fast, 30 for Slow)
    m_periods = min(30, lookback // 2) 

    # 2. Use m_periods HERE (not the number 30)
    mean = data.rolling(window=lookback, min_periods=m_periods).mean()
    std = data.rolling(window=lookback, min_periods=m_periods).std()
    
    # 3. Standardize
    z = (data - mean) / (std + 1e-8)
    
    return z.replace([np.inf, -np.inf], 0).fillna(0)




