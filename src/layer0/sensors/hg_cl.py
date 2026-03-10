import numpy as np

def copper_oil(prices):

    hg = prices["HG=F"]
    cl = prices["CL=F"]

    return np.log(hg) - np.log(cl)
