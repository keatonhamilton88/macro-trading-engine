import pandas as pd
import numpy as np

def zscore_returns(series, lookback=252):
    returns = series.pct_change()
    mean = returns.rolling(lookback).mean()
    std = returns.rolling(lookback).std()
    z = (returns - mean) / std
    return z

