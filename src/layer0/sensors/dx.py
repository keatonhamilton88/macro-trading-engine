import numpy as np

def dx_sensor(prices):

    dxy = prices["DX-Y.NYB"]

    return np.log(dxy)
