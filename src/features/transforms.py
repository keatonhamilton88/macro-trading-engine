import pandas as pd
import numpy as np

def zscore_returns(series, lookback=252):
    returns = series.pct_change()
    mean = returns.rolling(lookback).mean()
    std = returns.rolling(lookback).std()
    # Adding a tiny 1e-8 prevents division by zero
    z = (returns - mean) / (std + 1e-8)
    return z


