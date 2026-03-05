import pandas as pd
import numpy as np

def z_score(series, lookback=252):
    mean = series.rolling(lookback).mean()
    std = series.rolling(lookback).std()
    z = (series - mean) / std
    return z.dropna()