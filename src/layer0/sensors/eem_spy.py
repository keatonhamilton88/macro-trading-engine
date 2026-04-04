import numpy as np

def eem_spy(prices):
    if "EEM" not in prices or "TLT" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    eem = prices["EEM"].ffill()
    spy = prices["SPY"].ffill()

    return np.log(eem) - np.log(spy)
