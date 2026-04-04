import numpy as np
import pandas as pd 

def dx(prices):
    if "DX.Y.NYB" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    dxy = prices["DX-Y.NYB"].ffill()

    return np.log(dxy)
