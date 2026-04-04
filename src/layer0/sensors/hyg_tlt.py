import numpy as np
import pandas as pd 

def hyg_tlt(prices):
    if "HYG" not in prices or "TLT" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    hyg = prices["HYG"].ffill()
    tlt = prices["TLT"].ffill()

    return np.log(hyg) - np.log(tlt)
