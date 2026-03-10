import numpy as np

def hg_gc(prices):

    hg = prices["HG=F"]
    gc = prices["GC=F"]

    return np.log(hg) - np.log(gc)
