import numpy as np

def eur_chf(prices):
    if "EURCHF=X" not in prices:
        return pd.Series(index=prices.index, dtype=float)

    eurchf = prices["EURCHF=X"].ffill()

    return np.log(eurchf)
