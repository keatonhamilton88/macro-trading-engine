import numpy as np
import pandas as pd 

def usd_jpy(prices):
    if "JPY=X" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    usdjpy = prices["JPY=X"].ffill()

    return np.log(usdjpy)
