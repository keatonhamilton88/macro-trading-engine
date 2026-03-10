import numpy as np

def spy_tlt(prices):

    spy = prices["SPY"]
    tlt = prices["TLT"]

    return np.log(spy) - np.log(tlt)
