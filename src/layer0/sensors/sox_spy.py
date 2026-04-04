import numpy as np
import pandas as pd 

def sox_spy(prices):
    if "SOXX" not in prices or "SPY" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    sox = prices["SOXX"].ffill()
    spy = prices["SPY"].ffill()

    return np.log(sox) - np.log(spy)
