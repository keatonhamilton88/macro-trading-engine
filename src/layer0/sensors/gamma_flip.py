import numpy as np

def gamma_flip(prices):
    if not prices.empty:
        return pd.Series(0.0, index=prices.index, name='gamma_flip')
    else:
        return pd.Series(dtype=float)
