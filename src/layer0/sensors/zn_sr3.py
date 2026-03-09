import numpy as np

def zn_sr3_sensor(prices):

    zn = prices["ZN"]
    sr3 = prices["SR3"]

    return np.log(zn) - np.log(sr3)
