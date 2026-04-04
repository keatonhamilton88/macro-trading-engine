import numpy as np 

def eur_usd(prices):
    if "EURUSD=X" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    eurusd = prices["EURUSD=X"].ffill()

    return np.log(eurusd)
