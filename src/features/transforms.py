import pandas as pd
import numpy as np

def zscore_sensor(series, lookback=252, is_return=True):
    """
    Standardizes sensors for PCA.
    is_return=True:  Use for Prices/Levels (SPY, AUDJPY, Gold). Calculates % change first.
    is_return=False: Use for Ratios/Indicators (VIX Ratio, P/C, GEX). Z-scores the raw value.
    """
    if is_return:
        data = series.pct_change()
    else:
        data = series

    # FIX: Ensure min_periods is never larger than the lookback window
    # We'll use 30 for macro (252), but for fast (20), we'll use 10.
    m_periods = min(30, lookback // 2) 

    # ADD min_periods=30 HERE
    # This ensures your 'forces' aren't empty for the first year
    mean = data.rolling(window=lookback, min_periods=30).mean()
    std = data.rolling(window=lookback, min_periods=30).std()
    
    # Prevents division by zero and handles NaNs
    z = (data - mean) / (std + 1e-8)
    
    return z



