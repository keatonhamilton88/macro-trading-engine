import numpy as np

def ashr_spy(prices):
  if "ASHR" not in prices or "SPY" not in prices:
        return pd.Series(index=prices.index, dtype=float)

  ashr = prices["ASHR"]
  spy = prices["SPY"]

  return np.log(ashr) - np.log(spy)


  
