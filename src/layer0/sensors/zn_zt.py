import numpy as np

def zn_zt(prices):

    zn = prices["ZN=F"]
    zt = prices["ZT=F"]

    return np.log(zn) - np.log(zt)
