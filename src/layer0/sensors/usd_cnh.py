import numpy as np
import pandas as pd 

def usd_cnh(prices):
    if "CNY=X" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    usdcnh = prices["CNY=X"].ffill()

    return np.log(usdcnh)
