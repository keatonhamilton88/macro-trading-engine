import numpy as np

def cl_gc(prices):

    cl = prices["CL=F"]
    gc = prices["GC=F"]

    return np.log(cl) - np.log(gc)
