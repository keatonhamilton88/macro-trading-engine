import numpy as np

def hg_cl(prices):

    hg = prices["HG=F"]
    cl = prices["CL=F"]

    return np.log(hg) - np.log(cl)
