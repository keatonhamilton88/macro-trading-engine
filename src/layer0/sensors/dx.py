import numpy as np

def dollar_sensor(prices):

    dxy = prices["DX-Y.NYB"]

    return np.log(dxy)
