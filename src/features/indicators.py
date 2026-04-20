import pandas as pd
import numpy as np

def compute_rsi(series, window=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

def compute_ema(series, window):
    return series.ewm(span=window, adjust=False).mean()

def compute_atr(df, window=14):
    """Calculates Average True Range for position sizing."""
    # Assuming df has 'High', 'Low', 'Close'
    tr1 = df['High'] - df['Low']
    tr2 = (df['High'] - df['Close'].shift()).abs()
    tr3 = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=window).mean()

def compute_bb_width(series, window=20, std_dev=2):
    """Measures 'The Squeeze' - lower values mean a breakout is coming."""
    ma = series.rolling(window=window).mean()
    sd = series.rolling(window=window).std()
    upper = ma + (std_dev * sd)
    lower = ma - (std_dev * sd)
    return (upper - lower) / ma
