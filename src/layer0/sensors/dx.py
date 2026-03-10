import numpy as np

def dx(prices):

    dxy = prices["DX-Y.NYB"]

    return np.log(dxy)
