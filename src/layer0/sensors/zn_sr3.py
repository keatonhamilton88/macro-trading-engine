import numpy as np
import pandas as pd 

def zn_sr3(prices):
    if "ZN=F" not in prices or "SR3=F" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    zn = prices["ZN=F"].ffill()
    sr3 = prices["SR3=F"].ffill()

    return np.log(zn) - np.log(sr3)
