import numpy as np
import pandas as pd 

def hg_tio(prices):
    if "HG=F" not in prices or "TIO=F" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    hg = prices["HG=F"].ffill()
    tio = prices["TIO=F"].ffill()

    return np.log(hg) - np.log(tio)
