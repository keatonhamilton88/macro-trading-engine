import numpy as np

def copper_gold_sensor(prices):

    hg = prices["HG=F"]
    gc = prices["GC=F"]

    return np.log(hg) - np.log(gc)
