import numpy as np

def spy_tlt_sensor(prices):

    spy = prices["SPY"]
    tlt = prices["TLT"]

    return np.log(spy) - np.log(tlt)
