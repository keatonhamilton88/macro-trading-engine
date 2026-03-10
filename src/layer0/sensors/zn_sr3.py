import numpy as np

def zn_sr3(prices):

    zn = prices["ZN=F"]
    sr3 = prices["SR3=F"]

    return np.log(zn) - np.log(sr3)
