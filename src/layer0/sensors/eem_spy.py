import numpy as np
import pandas as pd 

def eem_spy(prices):
    if "EEM" not in prices or "SPY" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    eem = prices["EEM"].ffill()
    spy = prices["SPY"].ffill()

    return np.log(eem) - np.log(spy)
