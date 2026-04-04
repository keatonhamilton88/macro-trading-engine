import numpy as np

def spy_tlt(prices):
    if "SPY" not in prices or "TLT" not in prices:
        return pd.Series(index=prices.index, dtype=float)
    
    spy = prices["SPY"]
    tlt = prices["TLT"]

    return np.log(spy) - np.log(tlt)
