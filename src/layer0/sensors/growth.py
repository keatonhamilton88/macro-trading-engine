import numpy as np

def growth_sensor(prices):

    hg = prices["HG=F"]
    gc = prices["GC=F"]

    return np.log(hg) - np.log(gc)
