import numpy as np

def ashr_spy(prices):

  ashr = prices["ASHR"]
  spy = prices["SPY"]

  return np.log(ashr) - np.log(spy)


  
