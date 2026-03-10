import numpy as np

def copper_gold(prices):

    hg = prices["HG=F"]
    gc = prices["GC=F"]

    return np.log(hg) - np.log(gc)
