import numpy as np

def eem_spy(prices):

    eem = prices["EEM"]
    spy = prices["SPY"]

    return np.log(eem) - np.log(spy)
