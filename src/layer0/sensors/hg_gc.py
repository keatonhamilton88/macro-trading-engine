import numpy as np
import pandas as pd 

def hg_gc(prices):
    if "HG=F" not in prices or "GC=F" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    hg = prices["HG=F"].ffill()
    gc = prices["GC=F"].ffill()

    return np.log(hg) - np.log(gc)
