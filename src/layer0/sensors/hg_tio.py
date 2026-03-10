import numpy as np

def hg_tio(prices):

    hg = prices["HG=F"]
    tio = prices["TIO=F"]

    return np.log(hg) - np.log(tio)
