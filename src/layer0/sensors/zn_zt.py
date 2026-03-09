import numpy as np

def zn_zt_sensor(prices):

    zn = prices["ZN"]
    zt = prices["ZT"]

    return np.log(zn) - np.log(zt)
