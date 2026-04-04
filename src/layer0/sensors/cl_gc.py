import numpy as np
import pandas as pd 

def cl_gc(prices):
    if "CL=F" not in prices or "GC=F" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    cl = prices["CL=F"].ffill()
    gc = prices["GC=F"].ffill()

    return np.log(cl) - np.log(gc)
