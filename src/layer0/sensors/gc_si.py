import numpy as np
import pandas as pd 

def gc_si(prices):
    if "GC=F" not in prices or "SI=F" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    gc = prices["GC=F"].ffill()
    si = prices["SI=F"].ffill()
  
    return np.log(gc) - np.log(si)
