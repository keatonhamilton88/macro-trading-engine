import numpy as np

def em_sensor(prices):

    eem = prices["EEM"]
    spy = prices["SPY"]

    return np.log(eem) - np.log(spy)
