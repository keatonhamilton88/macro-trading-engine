import numpy as np
import pandas as pd 

def zn_zt(prices):\
    if "ZN=F" not in prices or "ZT=F" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    zn = prices["ZN=F"].ffill()
    zt = prices["ZT=F"].ffill()

    return np.log(zn) - np.log(zt)
