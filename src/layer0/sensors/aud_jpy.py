import numpy as np

def aud_jpy(prices):
    if "AUDJPY=X" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    audjpy = prices["AUDJPY=X"].ffill()

    return np.log(audjpy)
