import numpy as np

def aud_jpy(prices):
    if "AUD" not in prices or "JPY" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    audjpy = prices["AUDJPY=X"]

    return np.log(audjpy)
