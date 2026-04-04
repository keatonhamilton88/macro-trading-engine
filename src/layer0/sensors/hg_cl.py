import numpy as np

def hg_cl(prices):
    if "HG=F" not in prices or "CL=F" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    hg = prices["HG=F"].ffill()
    cl = prices["CL=F"].ffill()

    return np.log(hg) - np.log(cl)
